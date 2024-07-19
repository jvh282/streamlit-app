 # Importing required packages
import streamlit as st
import user_persona
import company_info
import openai_model
import data
import explain


PAGES = {
    "Erklärung": explain,
    "User Persona": user_persona,
    "Company Information": company_info,
    "Data": data,
    "OpenAI Model": openai_model,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()