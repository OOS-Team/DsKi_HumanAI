import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Definiert die Berechtigungen, die von der Gmail API angefordert werden.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_api(credentials_path='credentials/google_credentials.json'):
    """Authentifiziert den Benutzer bei der Gmail API und erstellt ein Service-Objekt."""
    creds = None
    # Lädt vorhandene Zugriffstoken aus 'token.pickle', falls vorhanden.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Wenn keine gültigen Credentials vorhanden sind, startet der Login-Prozess.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Speichert die neuen Credentials für zukünftige Läufe.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_plain_text_from_payload(part):
    """Extrahiert rekursiv den Klartext aus dem E-Mail-Body."""
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

def list_new_messages(service, user_id='me', history_id=None):
    """Listet neue Nachrichten seit dem letzten bekannten History-ID."""
    try:
        response = service.users().history().list(userId=user_id, startHistoryId=history_id).execute()
        changes = response.get('history', [])
        message_ids = [change['messages'][0]['id'] for change in changes if 'messages' in change]
        return message_ids
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_message_details(service, user_id, message_id):
    """Ruft die Details einer spezifischen Nachricht ab, einschließlich Betreff, Absender und Klartext-Body."""
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='full').execute()

        # Extrahiert den Payload der E-Mail und dann die Headers.
        payload = message.get('payload', {})
        headers = payload.get('headers', [])  # Hier wird die 'headers'-Variable korrekt definiert.

        # Ermittelt den Betreff und den Absender der E-Mail aus den Headern.
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        sender = next((header['value'] for header in headers if header['name'] == 'From'), None)

        # Extrahiert den Klartext-Body aus dem Payload.
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
    """Markiert eine Nachricht als gelesen."""
    try:
        service.users().messages().modify(userId=user_id, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')

# Weitere Hilfsfunktionen für die Gmail-Integration können hier hinzugefügt werden.
