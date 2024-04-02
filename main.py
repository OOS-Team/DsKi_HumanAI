from src.gmail_integration import authenticate_gmail_api, list_new_messages, get_message_details, mark_message_as_read
import time
import os  # Für Verzeichnisoperationen

# Pfad zu den Anmeldedaten ersetzen
CREDENTIALS_PATH = 'credentials/google_credentials.json'

# Verzögerung zwischen jeder Überprüfung des Posteingangs festlegen (z.B. 60 Sekunden)
CHECK_INTERVAL = 60

# Ordnerpfad für gespeicherte E-Mails
EMAIL_SAVE_PATH = 'emails/inbox'

def process_email_content(email_body):
    # Platzhalter für die Verarbeitung mit der OpenAI API
    summarized_content = email_body  # Ersetzen mit dem tatsächlichen Aufruf der OpenAI API
    return summarized_content

def send_to_whatsapp(summarized_content):
    print("Sending to WhatsApp:", summarized_content)  # Ersetzen mit dem tatsächlichen API-Aufruf

def main():
    # Authentifizieren und den Gmail-API-Dienst erstellen
    service = authenticate_gmail_api(CREDENTIALS_PATH)

    # Stellen Sie sicher, dass der Ordner für E-Mails existiert
    if not os.path.exists(EMAIL_SAVE_PATH):
        os.makedirs(EMAIL_SAVE_PATH)

    # Die aktuellste History-ID abrufen
    profile = service.users().getProfile(userId='me').execute()
    history_id = profile.get('historyId')

    while True:
        # Neue Nachrichten seit der zuletzt gespeicherten History-ID abrufen
        new_messages = list_new_messages(service, history_id=history_id)

        # Jede neue Nachricht verarbeiten
        for message_id in new_messages:
            details = get_message_details(service, 'me', message_id)
            if details:
                # Inhalt der E-Mail in einer .txt-Datei im Ordner 'emails/inbox' speichern
                filename = os.path.join(EMAIL_SAVE_PATH, f"email_{message_id}.txt")
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"From: {details['sender']}\n")
                    file.write(f"Subject: {details['subject']}\n")
                    file.write(f"Body:\n{details['body']}\n")
                
                # Optional die Nachricht als gelesen markieren
                mark_message_as_read(service, 'me', message_id)
                
        # Die History-ID für die nächste Überprüfung aktualisieren
        profile = service.users().getProfile(userId='me').execute()
        history_id = profile.get('historyId')

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
