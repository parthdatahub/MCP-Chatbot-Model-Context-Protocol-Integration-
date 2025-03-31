import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import io
import fitz  # PyMuPDF
import pandas as pd
import docx

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    creds = None
    if os.path.exists('token_drive.pkl'):
        with open('token_drive.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_drive.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def list_drive_files():
    service = authenticate_google_drive()
    results = service.files().list(
        pageSize=20,
        fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    return [f"{file['name']} | {file['id']}" for file in files]

def get_file_content_from_drive(selected_file):
    service = authenticate_google_drive()
    file_name, file_id = selected_file.split(" | ")
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext == ".pdf":
        return fitz.open(stream=fh.read(), filetype="pdf").get_page_text(0)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(fh)
        return df.to_string(index=False)
    elif ext == ".docx":
        doc = docx.Document(fh)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return f"Unsupported file format: {ext}"
