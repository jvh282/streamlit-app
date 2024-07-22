# Setup Instructions 🚀

This folder contains the necessary environment to run a Chatbot powered by OpenAI within a Streamlit Dashboard application. Please note that this folder includes secret API keys for an HdM-OpenAI account. Use this app exclusively for educational purposes in our course and do not share these keys with others.

## How to Start the Chatbot

To operate the app, perform the following steps within a Visual Studio Code environment:

1. **Create Your Assistant**:
   - Navigate to the **assistant-gpt** folder.
   - Open the `assistant-create.ipynb` notebook and execute the instructions to generate your Assistant. Ensure to copy the Assistant ID once created.

2. **Configure Environment Variables**:
   - Open the `.env` file within the same folder.
   - Replace `INSERT YOUR ASSISTANT ID` with the Assistant ID you copied earlier in the line:

     ```bash
     OPENAI_ASSISTANT='INSERT YOUR ASSISTANT ID'
     ```

   - Save your changes and keep the remaining content unchanged.

3. **Launch the Application**:
   - For Windows users: Open the Anaconda Command Prompt and navigate to the **assistant-gpt** directory.
   - For VS Code users: Open the integrated Terminal via the VS Code menu.
   - In the command line, enter:

     ```bash
     streamlit run app.py
     ```

   - This command should open your browser and direct you to a login page.

4. **Log In**:
   - On the login page, enter the following credentials:
     - AI Tutor: `CustomGPT`
     - Password: `123`

You are now ready to interact with your Chatbot!

## How to Update Your Chatbot's Instructions

To update the instructions for your Chatbot:

- Open the `assistant-update.ipynb` notebook in the **assistant-gpt** folder.
- Follow the provided steps to modify and update your Chatbot's configuration.