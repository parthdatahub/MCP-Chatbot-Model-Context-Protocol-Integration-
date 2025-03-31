from O365 import Account, FileSystemTokenBackend
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client_id = os.getenv("OUTLOOK_CLIENT_ID")
tenant_id = os.getenv("OUTLOOK_TENANT_ID")
redirect_uri = os.getenv("OUTLOOK_REDIRECT_URI")

print("Client ID:", client_id)
print("Tenant ID:", tenant_id)
print("Redirect URI:", redirect_uri)

if not all([client_id, tenant_id, redirect_uri]):
    raise ValueError("Missing one of CLIENT_ID, TENANT_ID or REDIRECT_URI")

credentials = (client_id, )

token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')

account = Account(
    credentials,
    auth_flow_type='public',
    tenant_id=tenant_id,
    token_backend=token_backend
)

if not account.is_authenticated:
    account.authenticate(
        scopes=['offline_access', 'https://graph.microsoft.com/Mail.Read'],
        redirect_uri=redirect_uri
    )

def get_email_context(limit=5, folder="Inbox"):
    mailbox = account.mailbox()

    if folder.lower() == "sent":
        folder_obj = mailbox.sent_folder()
    else:
        folder_obj = mailbox.inbox_folder()

    messages = folder_obj.get_messages(limit=limit)

    email_data = ""
    for msg in messages:
        email_data += f"Subject: {msg.subject}\nPreview: {msg.body_preview}\n\n"

    return email_data

# ✅ Safe test block
if __name__ == "__main__":
    print("🔍 Testing email fetch (standalone)...")
    print(get_email_context(limit=5, folder="Inbox"))
