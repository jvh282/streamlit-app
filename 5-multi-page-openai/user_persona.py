# user_persona.py
import streamlit as st

def app():
    st.title('User Persona Creation')

    # Eingabefelder für grundlegende Informationen der User Persona
    with st.form(key='user_persona_form'):
        name = st.text_input("Name der Persona")
        alter = st.slider("Alter", 18, 100, 30)  # Min, Max, Default
        geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers", "Keine Angabe"])
        ansprache = st.selectbox("Ansprache", ["Persönlich", "Allgemein"])
        anrede = st.selectbox("Anrede",["Duzen", "Siezen"])

        # Psychografische Daten
        interessen = st.text_area("Interessen und Hobbys")
        werte = st.text_area("Werte und Einstellungen")
        beruf= st.text_area("Beruf")
        

        # Verhaltensdaten
        nutzung_sozialer_medien = st.text_area("Nutzungsverhalten Sozialer Medien")
        markenpraferenzen = st.text_area("Markenpräferenzen")
        markenloyalitaet= st.text_input ("Markenloyalität")


        # Knopf zum Absenden des Formulars
        submit_button = st.form_submit_button("User Persona erstellen")

        if submit_button:
            # Speichern der Persona-Daten im session_state
            st.session_state['persona_data'] = {
                "name": name,
                "alter": alter,
                "geschlecht": geschlecht,
                "interessen": interessen,
                "werte": werte,
                "einkaufsgewohnheiten": einkaufsgewohnheiten,
                "nutzung_sozialer_medien": nutzung_sozialer_medien,
                "markenpraferenzen": markenpraferenzen,
                "markenloyalitaet": markenloyalitaet,
                "ansprache": ansprache,
                "anrede": anrede
            }

            st.success("User Persona erfolgreich erstellt!")

# Dieser Teil ist für Testzwecke, wenn Sie dieses Skript einzeln laufen lassen.
if __name__ == "__main__":
    app()
