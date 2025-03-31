# MCP Chatbot Setup

1. Create a virtual environment
2. Install dependencies
3. Configure your .env file
4. Run `streamlit run app.py`

![image](https://github.com/user-attachments/assets/c2e4a18e-2672-4ea3-b0ce-df1f37308bee)


# MCP Chatbot 🧠 (Model Context Protocol Integration)

This project is a fully working chatbot powered by **Azure OpenAI GPT-4o** and designed to follow the principles of the **MCP (Model Context Protocol)**, enabling seamless integration of contextual data from various sources like:

- 📬 **Outlook Emails** (Inbox & Sent)
- 📁 **Local Files** (PDFs, Excel, DOCX, etc.)
- ☁️ **Google Drive** (read-only content)
- 💬 **Microsoft Teams** (chat support in progress)

---

## 🌐 Streamlit Chat UI
Run locally:
```bash
streamlit run app.py
```

---

## 📚 Key Features

| Source             | Status       | Purpose |
|--------------------|--------------|---------|
| Outlook Email      | ✅ Integrated | Brings email messages as context to GPT |
| Local File Support | ✅ Integrated | Reads local PDFs, Excel, Word files for context |
| Google Drive Files | ✅ Integrated | Authenticated access to Drive files as context |
| MS Teams Messages  | ⏳ In Progress | Context from personal/team messages |

---

## 🚀 Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/mcp-chatbot.git
cd mcp-chatbot
```

### 2. Create Virtual Environment
```bash
conda create -n MCP_Pro python=3.10 -y
conda activate MCP_Pro
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a file named `.env`:
```env
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
DEPLOYMENT_NAME=gpt-4o-mini
API_KEY=your_azure_openai_key
OUTLOOK_CLIENT_ID=your_outlook_app_id
OUTLOOK_TENANT_ID=your_tenant_id
OUTLOOK_REDIRECT_URI=https://login.microsoftonline.com/common/oauth2/nativeclient
```

---

## ☁️ Google Drive Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Set up OAuth consent screen > Add scopes > Add test users
- Create OAuth Client ID (Desktop App) and download `credentials.json`
- Save it in the root project directory

Run:
```bash
python test_drive.py
```
This creates a `token_drive.pkl` for future Drive access.

---

## 📁 Project Structure
```
app.py                      # Main Streamlit UI
ask_ai.py                  # GPT-4o response builder using context
mcp_outlook.py             # Outlook email integration
mcp_google_drive.py        # Google Drive integration
local_utils.py             # Local file reading (PDF, DOCX, XLSX)
mcp_team.py                # Teams message support (coming soon)
requirements.txt           # Python dependencies
.env.template              # Sample .env file
README.md                  # This file
```

---

## 📌 Purpose
This project showcases how the **MCP (Model Context Protocol)** can be implemented in a real-world application to allow GPT models to consume dynamic, multi-source context — including emails, documents, and chat systems.

---

## 🛡️ Disclaimer
This chatbot runs locally and does not store any uploaded content. Ensure proper token and data handling before deploying to production.

---

## 👨‍💻 Built By
Created by [Parth Gajmal](mailto:prgajmal@gmail.com)
- GPT-4o via Azure OpenAI
- Microsoft Graph API
- Google OAuth
- MCP context pipeline architecture
- Streamlit for UI

---

## 🛣️ Roadmap
- [x] Outlook email context integration
- [x] Local file context extraction
- [x] Google Drive integration
- [ ] Teams chat integration (direct + channel)
- [ ] Additional connectors (e.g. SharePoint, OneDrive)

---

## 🔮 Future Enhancements
• Add **Slack**, **Jira**, **Notion**  
• Connect to **databases** (MySQL, PostgreSQL, MongoDB, etc.)  
• Add **user roles & access control**  
• **RAG + Vector DB integration** (FAISS, Pinecone, Weaviate, etc.)  
• Integrate with **SharePoint**  
• Support for **OneDrive**  
• Connect to **Dropbox**, **Box**, **iCloud Drive**  
• Support for **Trello**, **Asana**, **ClickUp**  
• CRM integration: **Salesforce**, **Zoho**, **HubSpot**  
• Embed inside **Microsoft Teams as a bot**  
• Integrate with **WhatsApp**, **Telegram**, **Discord**  
• Support **CSV and JSON** structured data  
• Enable **scheduled context refresh** from connected sources  
• Build **admin dashboard** for monitoring & analytics  

---

## 🧾 License
MIT License

