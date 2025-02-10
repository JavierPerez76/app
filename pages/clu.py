import streamlit as st
import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

# Cargar variables de entorno
load_dotenv()
ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

# Cliente de Azure
client = ConversationAnalysisClient(ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))

# Configuración del proyecto
cls_project = "VanguardiasPremium"
deployment_slot = "production"

st.title("Análisis de Conversaciones con CLU")
st.info("🔍 Introduce un texto y analiza su intención.")

# Entrada de texto del usuario
user_input = st.text_area("Escribe tu texto aquí:")

if st.button("Analizar"):
    if user_input:
        with client:
            result = client.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": user_input
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": cls_project,
                        "deploymentName": deployment_slot,
                        "verbose": True
                    }
                }
            )

        # Extraer intención y entidades
        top_intent = result["result"]["prediction"]["topIntent"]
        confidence = result["result"]["prediction"]["intents"][0]["confidenceScore"]
        entities = result["result"]["prediction"]["entities"]

        # Mostrar resultados
        st.subheader("Resultado del Análisis:")
        st.write(f"**Intención Detectada:** {top_intent}")
        st.write(f"**Confianza:** {confidence:.2f}")

        # Mostrar entidades si existen
        if entities:
            st.subheader("Entidades Detectadas:")
            for entity in entities:
                st.write(f"📌 **Categoría:** {entity['category']} | **Texto:** {entity['text']} | **Confianza:** {entity['confidenceScore']:.2f}")
        
        # Ejecutar función según intención
        if top_intent == 'GetTime':
            location = 'local'
            for entity in entities:
                if entity["category"] == "Location":
                    location = entity["text"]
            st.write(f"⏰ **Hora en {location}:** {GetTime(location)}")

        elif top_intent == 'GetDay':
            date_string = "02/10/2025"
            for entity in entities:
                if entity["category"] == "Date":
                    date_string = entity["text"]
            st.write(f"📅 **Día de la fecha {date_string}:** {GetDay(date_string)}")

        elif top_intent == 'GetDate':
            day = "today"
            for entity in entities:
                if entity["category"] == "Weekday":
                    day = entity["text"]
            st.write(f"📆 **Fecha para {day}:** {GetDate(day)}")

        else:
            st.warning("⚠️ Intención no reconocida. Prueba preguntando sobre la hora, el día o la fecha.")
    else:
        st.warning("⚠️ Ingresa un texto antes de analizar.")

# Funciones auxiliares para GetTime, GetDate y GetDay
from datetime import datetime, timedelta, date, timezone

def GetTime(location):
    now = datetime.now(timezone.utc)
    locations = {
        "local": now,
        "london": now,
        "sydney": now + timedelta(hours=11),
        "new york": now + timedelta(hours=-5),
        "nairobi": now + timedelta(hours=3),
        "tokyo": now + timedelta(hours=9),
        "delhi": now + timedelta(hours=5.5),
    }
    return locations.get(location.lower(), "Ubicación desconocida").strftime('%H:%M')

def GetDate(day):
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }
    today = date.today()
    if day.lower() == 'today':
        return today.strftime("%m/%d/%Y")
    elif day.lower() in weekdays:
        return (today + timedelta(days=(weekdays[day.lower()] - today.weekday()))).strftime("%m/%d/%Y")
    return "Fecha desconocida"

def GetDay(date_string):
    try:
        return datetime.strptime(date_string, "%m/%d/%Y").strftime("%A")
    except:
        return "Formato incorrecto (MM/DD/YYYY)"
