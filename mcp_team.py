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

# Credentials without client secret (public/native app)
credentials = (client_id,)

# Token storage backend
backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token_teams.txt')

# Create account with delegated flow
delegated_account = Account(
    credentials,
    auth_flow_type='public',
    tenant_id=tenant_id,
    token_backend=backend
)

if not delegated_account.is_authenticated:
    requested_scopes = [
        'https://graph.microsoft.com/User.Read',
        'https://graph.microsoft.com/Chat.Read',
        'https://graph.microsoft.com/Chat.ReadWrite',
        'https://graph.microsoft.com/ChannelMessage.Read.All',
        'https://graph.microsoft.com/ChannelMessage.Send',
        'https://graph.microsoft.com/offline_access'
    ]

    consent_url, state = delegated_account.con.get_authorization_url(
        requested_scopes,
        redirect_uri=redirect_uri,
        prompt='consent'
    )

    print("👉 Visit this URL in browser and login:\n", consent_url)
    redirected_url = input("🔐 Paste the full redirected URL here:\n")
    delegated_account.con.request_token(redirected_url, redirect_uri=redirect_uri)

# Teams chat logic
mailbox = delegated_account.mailbox()

# Fetch latest personal chat messages
def get_personal_chat_messages(limit=5):
    chats = delegated_account.connection.get('https://graph.microsoft.com/v1.0/me/chats')
    chat_list = chats.json().get('value', [])
    result = []

    for chat in chat_list[:limit]:
        chat_id = chat['id']
        messages_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages?$top=3"
        messages = delegated_account.connection.get(messages_url)
        messages_data = messages.json().get('value', [])

        for msg in messages_data:
            result.append({
                'chat_id': chat_id,
                'from': msg.get('from', {}).get('user', {}).get('displayName', 'Unknown'),
                'body': msg.get('body', {}).get('content', '')
            })
    return result

# Send a message to a personal chat
def send_message_to_chat(chat_id, message_text):
    url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
    payload = {
        "body": {
            "content": message_text
        }
    }
    response = delegated_account.connection.post(url, json=payload)
    return response.status_code == 201

# Sample test
if __name__ == '__main__':
    print("\n📥 Last messages from chats:")
    messages = get_personal_chat_messages()
    for m in messages:
        print(f"From: {m['from']} | Msg: {m['body'][:50]}... | Chat ID: {m['chat_id']}")

    # Uncomment to test send
    # send_message_to_chat(messages[0]['chat_id'], "Hello from MCP Chatbot!")
