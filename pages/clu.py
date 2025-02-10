import os
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta, date, timezone
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import QuestionAnsweringClient

# Function for getting time based on location
def GetTime(location):
    time_string = ''
    if location.lower() == 'local':
        now = datetime.now()
        time_string = '{}:{:02d}'.format(now.hour, now.minute)
    elif location.lower() == 'london':
        utc = datetime.now(timezone.utc)
        time_string = '{}:{:02d}'.format(utc.hour, utc.minute)
    elif location.lower() == 'sydney':
        time = datetime.now(timezone.utc) + timedelta(hours=11)
        time_string = '{}:{:02d}'.format(time.hour, time.minute)
    elif location.lower() == 'new york':
        time = datetime.now(timezone.utc) + timedelta(hours=-5)
        time_string = '{}:{:02d}'.format(time.hour, time.minute)
    elif location.lower() == 'nairobi':
        time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_string = '{}:{:02d}'.format(time.hour, time.minute)
    elif location.lower() == 'tokyo':
        time = datetime.now(timezone.utc) + timedelta(hours=9)
        time_string = '{}:{:02d}'.format(time.hour, time.minute)
    elif location.lower() == 'delhi':
        time = datetime.now(timezone.utc) + timedelta(hours=5.5)
        time_string = '{}:{:02d}'.format(time.hour, time.minute)
    else:
        time_string = "I don't know what time it is in {}".format(location)
    
    return time_string

# Function to get date based on the day
def GetDate(day):
    date_string = 'I can only determine dates for today or named days of the week.'
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    today = date.today()
    day = day.lower()
    if day == 'today':
        date_string = today.strftime("%m/%d/%Y")
    elif day in weekdays:
        todayNum = today.weekday()
        weekDayNum = weekdays[day]
        offset = weekDayNum - todayNum
        date_string = (today + timedelta(days=offset)).strftime("%m/%d/%Y")

    return date_string

# Function to get day from date string
def GetDay(date_string):
    try:
        date_object = datetime.strptime(date_string, "%m/%d/%Y")
        day_string = date_object.strftime("%A")
    except:
        day_string = 'Enter a date in MM/DD/YYYY format.'
    return day_string

# Main function for the Streamlit app
def main():
    # Load environment variables
    load_dotenv()
    ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
    ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

    # Streamlit UI
    st.title("Azure Language Understanding in Streamlit")
    userText = st.text_input('Enter some text ("quit" to stop)')

    if userText.lower() != 'quit' and userText:
        try:
            # Create a client for the Language service model
            client = QuestionAnsweringClient(
                ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))

            # Call the Language service model to get intent and entities
            cls_project = 'VanguardiasPremium'
            deployment_slot = 'production'

            with client:
                query = userText
                result = client.analyze_conversation(
                    task={
                        "kind": "Conversation",
                        "analysisInput": {
                            "conversationItem": {
                                "participantId": "1",
                                "id": "1",
                                "modality": "text",
                                "language": "en",
                                "text": query
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

            top_intent = result["result"]["prediction"]["topIntent"]
            entities = result["result"]["prediction"]["entities"]

            # Display results
            st.write("Top intent: {}".format(top_intent))
            for entity in entities:
                st.write(f"Entity category: {entity['category']}, Text: {entity['text']}, Confidence score: {entity['confidenceScore']}")

            # Apply the appropriate action
            if top_intent == 'GetTime':
                location = 'local'
                if entities:
                    for entity in entities:
                        if 'Location' == entity["category"]:
                            location = entity["text"]
                st.write(f"The time in {location} is: {GetTime(location)}")

            elif top_intent == 'GetDay':
                date_string = date.today().strftime("%m/%d/%Y")
                if entities:
                    for entity in entities:
                        if 'Date' == entity["category"]:
                            date_string = entity["text"]
                st.write(f"The day for {date_string} is: {GetDay(date_string)}")

            elif top_intent == 'GetDate':
                day = 'today'
                if entities:
                    for entity in entities:
                        if 'Weekday' == entity["category"]:
                            day = entity["text"]
                st.write(f"The date for {day} is: {GetDate(day)}")

            else:
                st.write('Try asking me for the time, the day, or the date.')

        except Exception as ex:
            st.error(f"An error occurred: {ex}")

if __name__ == "__main__":
    main()
