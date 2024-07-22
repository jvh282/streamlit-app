# YOU DONT NEED TO CHANGE ANYTHING IN THIS CODE

import streamlit as st
import hmac
import openai
import uuid
import time
from openai import OpenAI
from assistant import gpts
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

#--------------------------------------------
# LOGIN
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("AI Tutor", key="gpt")
            st.text_input("Passwort", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["gpt"] in st.secrets["passwords"] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["gpt"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["logged_in_user"] = st.session_state["gpt"]  
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False


    if st.session_state.get("password_correct", False):
        return True


    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 AI Tutor nicht bekannt oder Passwort falsch")
    return False

if not check_password():
    st.stop()

if "logged_in_user" in st.session_state:
    custom_gpt = st.session_state["logged_in_user"]

#-------------------------------------------
# SELECT CUSTOM GPT
custom_gpt = st.session_state["logged_in_user"]
assistent_id = gpts[custom_gpt]

#--------------------------------------------
# INITIALIZE OPENAI
client = OpenAI()
MODEL = "gpt-4-1106-preview"

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0

#--------------------------------------------
# APP STARTS HERE
st.set_page_config(page_title="AI Tutor")

# Sidebar
st.sidebar.title("AI Tutor")
st.sidebar.write(custom_gpt)
st.sidebar.write("*Bitte eine Anfrage zu dem entsprechendem Themengebiet in das Chatfenster eingeben*")
st.sidebar.divider()

#Initialize OpenAI
if "assistant" not in st.session_state:
     openai.api_key = os.getenv('OPENAI_API_KEY')
     st.session_state.assistant = openai.beta.assistants.retrieve(assistent_id)
     st.session_state.thread = client.beta.threads.create(
          metadata={'session_id': st.session_state.session_id}
      )

# Display chat messages
elif hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
    st.session_state.messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id
    )
    for message in reversed(st.session_state.messages.data):
        if message.role in ["user", "assistant"]:
            with st.chat_message(message.role):
                for content_part in message.content:
                    message_text = content_part.text.value
                    st.markdown(message_text)

# Chat input and message creation
if prompt := st.chat_input("Wie kann ich weiterhelfen?"):

    with st.chat_message('user'):
        st.write(prompt)

    message_data = {
        "thread_id": st.session_state.thread.id,
        "role": "user",
        "content": prompt
    }

    st.session_state.messages = client.beta.threads.messages.create(**message_data)

    st.session_state.run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )

    with st.spinner('Antwort wird generiert ...'):
        if st.session_state.retry_error < 3:
            time.sleep(1)
            st.rerun()


# Handle run status
if hasattr(st.session_state.run, 'status'):
    if st.session_state.run.status == "running":
        with st.chat_message('assistant'):
            st.write("Antwort wird erzeugt ...")
        if st.session_state.retry_error < 3:
            time.sleep(1)
            st.rerun()

    elif st.session_state.run.status == "failed":
        st.session_state.retry_error += 1
        with st.chat_message('assistant'):
            if st.session_state.retry_error < 3:
                st.write("Ausführung fehlgeschlagen, erneuter Versuch ...")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Fehler: Die OpenAI-API verarbeitet derzeit zu viele Anfragen. Bitte versuchen Sie es später erneut ...")

    elif st.session_state.run.status != "completed":
        st.session_state.run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=st.session_state.run.id,
        )
        if st.session_state.retry_error < 3:
            time.sleep(3)
            st.rerun()

#-------------------------------------------