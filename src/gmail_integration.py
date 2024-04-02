import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The SCOPES define which permissions to request from the Gmail API.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail_api(credentials_path='credentials/google_credentials.json'):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_plain_text_from_payload(payload):
    for part in payload.get('parts', []):
        mime_type = part.get('mimeType', '')
        body_data = part.get('body', {}).get('data', '')
        if mime_type == 'text/plain':
            return base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('utf-8')
        elif mime_type == 'multipart/alternative' or mime_type == 'multipart/mixed':
            return get_plain_text_from_payload(part)
    return ''  # Default return value if no plain text part found


def list_new_messages(service, user_id='me', history_id=None):
    try:
        # If history_id is provided, list messages that arrived after that history ID
        response = service.users().history().list(userId=user_id, startHistoryId=history_id).execute()
        changes = response.get('history', [])
        
        # Extracts message ids from changes
        message_ids = [change['messages'][0]['id'] for change in changes if 'messages' in change]
        return message_ids
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_message_details(service, user_id, message_id):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='full').execute()

        # Extracting the payload of the email and then the headers.
        payload = message.get('payload', {})
        headers = payload.get('headers', [])

        # Getting the Subject and Sender Email from the headers
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        sender = next((header['value'] for header in headers if header['name'] == 'From'), None)

        # Get the email body
        parts = payload.get('parts', [])
        body_data = ''
        if parts:
            part = parts[0]  # assuming first part is text/plain
            body_data = part['body'].get('data', '')
        else:
            body_data = payload.get('body', {}).get('data', '')

        # Fetch only the plaintext part of the email
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
    try:
        # Marks the message as read by removing the 'UNREAD' label
        service.users().messages().modify(userId=user_id, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')

# Other helper functions related to Gmail integration can be added here
