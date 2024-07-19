import streamlit as st
import openai
import os
from dotenv import load_dotenv, find_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()


def app():
    st.title('OpenAI Model')

    # Setze den OpenAI API-Schlüssel
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Initialisiere Session-Variablen
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "run" not in st.session_state:
        st.session_state.run = {"status": None}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "retry_error" not in st.session_state:
        st.session_state.retry_error = 0

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

    # Chat input and message creation
    if prompt := st.chat_input("How can I assist you?"):
        with st.chat_message('user'):
            st.write(prompt)

        # API-Anfrage an OpenAI
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # Beispiel-Modell
                prompt=prompt,
                max_tokens=150
            )

            message = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": message})

            with st.chat_message('assistant'):
                st.write(message)
        except Exception as e:
            st.error(f"Error: {e}")

    # Handle run status
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
            st.session_state.run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=st.session_state.run.id,
            )
            if st.session_state.retry_error < 3:
                time.sleep(3)
                st.rerun()

if __name__ == "__main__":
    app()
