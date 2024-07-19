# openai_model.py

import streamlit as st
import openai
import os
import uuid
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze den OpenAI API-Schlüssel
openai.api_key = os.getenv('OPENAI_API_KEY')

def app():
    st.title('OpenAI Model')

    # Initialisiere OpenAI-Client
    # (Es kann auch sinnvoll sein, dies nur zu machen, wenn es nicht bereits initialisiert ist)
    
    # Initialisiere Sitzungsglobalvariablen
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "run" not in st.session_state:
        st.session_state.run = {"status": None}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "retry_error" not in st.session_state:
        st.session_state.retry_error = 0

    # Initialize OpenAI assistant (Hier muss eventuell der OpenAI-Client initialisiert werden)
    if "assistant" not in st.session_state:
        st.session_state.assistant = openai.ChatCompletion

    # Anzeigen von Chat-Nachrichten
    if hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
        # Hier muss die Logik angepasst werden, um Nachrichten aus dem Thread abzurufen
        for message in reversed(st.session_state.messages):
            if message['role'] in ["user", "assistant"]:
                with st.chat_message(message['role']):
                    st.write(message['content'])

    # Vorbereiten des initialen Prompts
    if 'persona_data' in st.session_state and 'company_data' in st.session_state:
        persona_data = st.session_state['persona_data']
        company_data = st.session_state['company_data']

        persona_str = ", ".join([f"{key}: {value}" for key, value in persona_data.items()])
        company_str = ", ".join([f"{key}: {value}" for key, value in company_data.items()])

        initial_prompt = f"Create marketing text based on the User Persona ({persona_str}) and company data ({company_str})."
    else:
        initial_prompt = "Please provide User Persona and company information."

    st.text_area("Initial Prompt (copy and edit if needed):", initial_prompt, height=100)

    # Chat-Eingabe und Nachrichten-Erstellung
    if prompt := st.chat_input("How can I assist you?"):
        with st.chat_message('user'):
            st.write(prompt)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Beispiel-Modell, stelle sicher, dass dies das richtige Modell ist
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )

            message = response.choices[0].message['content'].strip()
            st.session_state.messages.append({"role": "assistant", "content": message})

            with st.chat_message('assistant'):
                st.write(message)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    app()
