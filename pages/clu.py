import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

# Configuración
ls_prediction_endpoint = st.secrets['LS_CONVERSATIONS_ENDPOINT']
ls_prediction_key = st.secrets['LS_CONVERSATIONS_KEY']

# Crear cliente de Azure CLU
client = ConversationAnalysisClient(
    ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))

st.title("Chatbot CLU - Vanguardias")
st.write("Este chatbot analiza la intención de tus preguntas usando Azure CLU.")

# Entrada de usuario
user_input = st.text_input("Escribe tu pregunta:")

if user_input:
    with client:
        response = client.analyze_conversation(
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
                    "projectName": "VanguardiasPremium",
                    "deploymentName": "production",
                    "verbose": True
                }
            }
        )
    
    # Extraer respuesta
    if response["result"]["prediction"]["intents"]:
        top_intent = response["result"]["prediction"]["topIntent"]
        confidence = response["result"]["prediction"]["intents"][0]["confidenceScore"]
        st.write(f"**Intento detectado:** {top_intent} (Confianza: {confidence:.2f})")
    else:
        st.write("No se detectó un intento.")
