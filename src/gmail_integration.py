import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_api(credentials_path='credentials/google_credentials.json'):
    """Authenticates the user with the Gmail API and creates a service object."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_plain_text_from_payload(part):
    """Extracts the plain text from the email's body recursively."""
    mime_type = part.get('mimeType', '')
    if mime_type == 'text/plain':
        body_data = part.get('body', {}).get('data', '')
        return base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('utf-8')
    elif mime_type.startswith('multipart/'):
        for sub_part in part.get('parts', []):
            text = get_plain_text_from_payload(sub_part)
            if text:
                return text
    return ''

def list_new_messages(service, user_id='me', history_id='latest'):
    """Lists new messages since the last known history ID."""
    try:
        response = service.users().history().list(userId=user_id, startHistoryId=history_id).execute()
        changes = response.get('history', [])
        message_ids = [change['messages'][0]['id'] for change in changes if 'messages' in change]
        return message_ids
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_message_details(service, user_id, message_id):
    """Fetches details of a specific message, including subject, sender, and body."""
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
        body = get_plain_text_from_payload(payload)
        return {
            'id': message_id,
            'subject': subject,
            'sender': sender,
            'body': body
        }
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def mark_message_as_read(service, user_id, message_id):
    """Marks a message as read."""
    try:
        service.users().messages().modify(userId=user_id, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')

# Further helper functions for Gmail integration can be added here.
