# page_four.py
import streamlit as st

def app():
    st.title('Data')

    # Check if persona_data is available in session state
    if 'persona_data' in st.session_state and 'company_data' in st.session_state:
        persona_data = st.session_state['persona_data']
        company_data = st.session_state['company_data']

        # Format persona data and company data as a plain text string
        persona_data_txt = "\n".join([f"{key}: {value}" for key, value in persona_data.items()])
        company_data_txt = "\n".join([f"{key}: {value}" for key, value in company_data.items()])

        # Display persona and company data using markdown for better readability
        st.text("Persona Data")
        st.markdown(f"```\n{persona_data_txt}\n```")
        st.text("Company Data")
        st.markdown(f"```\n{company_data_txt}\n```")

        # Create a button to download the persona and company data as a .txt file
        st.download_button(
            label="Download Persona and Company Data",
            data=f"Persona Data:\n{persona_data_txt}\n\nCompany Data:\n{company_data_txt}",
            file_name='persona_and_company_data.txt',
            mime='text/plain',
        )
    else:
        st.warning("No persona or company data found. Please create the necessary data on the respective pages first.")
