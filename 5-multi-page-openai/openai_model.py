import streamlit as st
import openai
import uuid
import time
from dotenv import load_dotenv, find_dotenv
import os

# Lade die .env-Datei, um den API-Schlüssel zu setzen
load_dotenv(find_dotenv())

# Hole den API-Schlüssel aus der Umgebungsvariable
openai.api_key = os.getenv('OPENAI_API_KEY')

if openai.api_key is None:
    st.error("API key is missing. Please set the OPENAI_API_KEY environment variable.")
    st.stop()  # Stoppe die Ausführung, wenn der API-Schlüssel fehlt

def app():
    st.title('OpenAI Model')

    # Initialisiere die Session-Statusvariablen
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "run" not in st.session_state:
        st.session_state.run = {"status": None}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "retry_error" not in st.session_state:
        st.session_state.retry_error = 0

    # Erstelle ein Thread, falls nicht vorhanden
    if "thread_id" not in st.session_state:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[]
        )
        st.session_state.thread_id = response['id']

    # Anzeigen der Chat-Nachrichten
    if hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
        response = openai.ChatCompletion.list_messages(
            chat_id=st.session_state.thread_id
        )
        for message in reversed(response['messages']):
            if message['role'] in ["user", "assistant"]:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])

    # Bereite den initialen Prompt vor
    if 'persona_data' in st.session_state and 'company_data' in st.session_state:
        persona_data = st.session_state['persona_data']
        company_data = st.session_state['company_data']

        persona_str = ", ".join([f"{key}: {value}" for key, value in persona_data.items()])
        company_str = ", ".join([f"{key}: {value}" for key, value in company_data.items()])

        initial_prompt = f"Erstelle Werbetext basierend auf der User Persona ({persona_str}) und Unternehmensdaten ({company_str})."
    else:
        initial_prompt = "Bitte geben Sie Informationen zur User Persona und zum Unternehmen ein."

    # Anzeigen des initialen Prompts
    st.text_area("Initialer Prompt (kopieren und bei Bedarf bearbeiten):", initial_prompt, height=100)

    # Chat-Eingabe und Nachrichten-Erstellung
    if prompt := st.chat_input("Wie kann ich Ihnen helfen?"):
        with st.chat_message('user'):
            st.write(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.session_state.run = response['id']

        if st.session_state.retry_error < 3:
            time.sleep(1)
            st.rerun()

    # Verarbeite den Status der Anfrage
    if hasattr(st.session_state.run, 'status'):
        if st.session_state.run.status == "running":
            placeholder = st.empty()
            with placeholder.container():
                with st.chat_message('assistant'):
                    st.write("Thinking ......")

        elif st.session_state.run.status == "failed":
            st.session_state.retry_error += 1
            with st.chat_message('assistant'):
                if st.session_state.retry_error < 3:
                    st.write("Run failed, retrying ......")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error("FAILED: The OpenAI API is currently processing too many requests. Please try again later ......")

        elif st.session_state.run.status != "completed":
            st.session_state.run = openai.ChatCompletion.retrieve(
                chat_id=st.session_state.thread_id,
                run_id=st.session_state.run
            )
            if st.session_state.retry_error < 3:
                time.sleep(3)
                st.rerun()

if __name__ == "__main__":
    app()
