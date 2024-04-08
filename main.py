from src.gmail_integration import authenticate_gmail_api, list_new_messages, get_message_details, mark_message_as_read
from src.llm_integration import rank_email_with_llm, save_llm_response
import time
import os
from concurrent.futures import ThreadPoolExecutor

CREDENTIALS_PATH = 'credentials/google_credentials.json'
CHECK_INTERVAL = 1  # seconds
EMAIL_SAVE_PATH = 'emails/inbox'
LLM_CONFIG = {
    'base_url': "http://0.0.0.0:4000",
    'api_key': "NULL"  # Replace with your API key if needed
}

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def process_email(service, message_id):
    details = get_message_details(service, 'me', message_id)
    if details:
        filename = os.path.join(EMAIL_SAVE_PATH, f"email_{message_id}.txt")
        email_content = f"From: {details['sender']}\nSubject: {details['subject']}\nBody:\n{details['body']}\n"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(email_content)

        # Uncomment the following lines if LLM processing is desired
        # llm_response = rank_email_with_llm(email_content, LLM_CONFIG)
        # save_llm_response(llm_response, 'emails/processed')

        mark_message_as_read(service, 'me', message_id)

def main():
    service = authenticate_gmail_api(CREDENTIALS_PATH)
    ensure_directory_exists(EMAIL_SAVE_PATH)

    profile = service.users().getProfile(userId='me').execute()
    history_id = profile.get('historyId')

    while True:
        new_messages = list_new_messages(service, history_id=history_id)

        with ThreadPoolExecutor() as executor:
            for message_id in new_messages:
                executor.submit(process_email, service, message_id)

        profile = service.users().getProfile(userId='me').execute()
        history_id = profile.get('historyId')

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
