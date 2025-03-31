import streamlit as st
from ask_ai import ask_gpt
from mcp_outlook import get_email_context
from local_utils import load_all_files_from_folder, extract_uploaded_file_content
from mcp_google_drive import list_drive_files, get_file_content_from_drive

st.set_page_config(page_title="MCP Chatbot", layout="wide")
st.title("🤖 Model Context Protocol Use-Case")

# Tabs: Outlook + Local Files + Google Drive
page = st.sidebar.radio("Choose Mode:", ["📬 Outlook Emails", "📁 Local File Q&A", "🌐 Google Drive Files"])

# --------------------- OUTLOOK CHATBOT ---------------------
if page == "📬 Outlook Emails":
    st.header("📬 Ask Questions on Outlook Emails")

    folder = st.selectbox("Select Folder", ["Inbox", "Sent"])
    num_emails = st.slider("How many emails to load?", 1, 20, 5)

    with st.spinner("📥 Loading emails from Outlook..."):
        st.session_state.email_data = get_email_context(limit=num_emails, folder=folder)

    st.text_area("📄 Email Context", st.session_state.email_data, height=300)

    user_question = st.text_input("❓ Ask something about your emails")
    if user_question:
        with st.spinner("💬 Generating answer using GPT..."):
            response = ask_gpt(user_question, st.session_state.email_data, source="email")
        st.success(response)

# --------------------- LOCAL FILE Q&A ---------------------
elif page == "📁 Local File Q&A":
    st.header("📁 Ask Questions on Local Files (PDF, Excel, Word)")

    st.subheader("📂 Load files from data/ folder")
    if st.button("🔄 Load All Files"):
        with st.spinner("Reading local folder files..."):
            st.session_state.local_context = load_all_files_from_folder("data")

    if "local_context" in st.session_state:
        st.text_area("📄 File Content", st.session_state.local_context[:3000], height=300)

        user_question = st.text_input("❓ Ask something about your files")
        if user_question:
            with st.spinner("💬 Generating answer using GPT..."):
                response = ask_gpt(user_question, st.session_state.local_context, source="file")
            st.success(response)

    st.subheader("📥 Or Upload a New File")
    uploaded_file = st.file_uploader("Drag & Drop File", type=["pdf", "xlsx", "xls", "docx"])
    if uploaded_file:
        with st.spinner("Processing uploaded file..."):
            content = extract_uploaded_file_content(uploaded_file)
            st.session_state.uploaded_content = content

    if "uploaded_content" in st.session_state:
        st.text_area("📄 Uploaded File Content", st.session_state.uploaded_content[:3000], height=300)

        user_question = st.text_input("❓ Ask something about the uploaded file")
        if user_question:
            with st.spinner("💬 Generating answer using GPT..."):
                response = ask_gpt(user_question, st.session_state.uploaded_content, source="file")
            st.success(response)

# --------------------- GOOGLE DRIVE FILE Q&A ---------------------
elif page == "🌐 Google Drive Files":
    st.header("🌐 Ask Questions from Google Drive Files")

    if st.button("📂 List My Drive Files"):
        with st.spinner("Fetching Drive file list..."):
            st.session_state.drive_files = list_drive_files()

    if "drive_files" in st.session_state:
        selected_file = st.selectbox("Choose a file to read", st.session_state.drive_files)

        if st.button("📖 Load Selected File"):
            with st.spinner("Reading file from Drive..."):
                content = get_file_content_from_drive(selected_file)
                st.session_state.drive_file_content = content

    if "drive_file_content" in st.session_state:
        st.text_area("📄 Drive File Content", st.session_state.drive_file_content[:3000], height=300)

        user_question = st.text_input("❓ Ask something about the Drive file")
        if user_question:
            with st.spinner("💬 Generating answer using GPT..."):
                response = ask_gpt(user_question, st.session_state.drive_file_content, source="file")
            st.success(response)