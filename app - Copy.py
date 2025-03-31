import streamlit as st
from ask_ai import ask_gpt
from mcp_outlook import get_email_context

st.set_page_config(page_title="📬 Ask Outlook - MCP Chatbot")
st.title("📨 📬 Ask Outlook - MCP AI Chatbot")

# Dropdown to choose email folder
folder_choice = st.selectbox("📂 Choose email folder:", ["Inbox", "Sent"])

# Load emails once per folder selection
if "email_data" not in st.session_state or st.session_state.get("last_folder") != folder_choice:
    with st.spinner(f"Fetching emails from {folder_choice}..."):
        st.session_state.email_data = get_email_context(limit=5, folder=folder_choice)
        st.session_state.last_folder = folder_choice

# User input
user_question = st.text_input("💬 Ask a question based on your selected emails:")

# GPT response
if user_question:
    with st.spinner("Thinking..."):
        response = ask_gpt(user_question, context=st.session_state.email_data)
    st.success("✅ Answer:")
    st.write(response)
