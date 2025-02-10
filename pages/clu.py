import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
import pandas as pd

# Main function for the Streamlit app
def main():
    # Load environment variables
    load_dotenv()
    ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
    ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

    # Streamlit UI
    st.title("Azure Language Understanding in Streamlit")

    if userText.lower() != 'quit' and userText:
        try:
            # Create a client for the Language service model
            client = ConversationAnalysisClient(
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

            # Display top intent
            st.subheader(f"Top Intent: {top_intent}")

            # Display entities in a table with consistent styling
            if entities:
                st.subheader("Entities Recognized:")
                # Prepare the data for a table
                entity_data = {
                    "Category": [entity['category'] for entity in entities],
                    "Text": [entity['text'] for entity in entities],
                    "Confidence Score": [entity['confidenceScore'] for entity in entities]
                }
                df_entities = pd.DataFrame(entity_data)

                # Display the table with default styling
                st.dataframe(df_entities)

            else:
                st.write("No entities recognized.")

        except Exception as ex:
            st.error(f"An error occurred: {ex}")

if __name__ == "__main__":
    main()
