from src.gmail_integration import authenticate_gmail_api, list_new_messages, get_message_details, mark_message_as_read
import time

# Replace 'credentials/google_credentials.json' with your actual path to the credentials file
CREDENTIALS_PATH = 'credentials/google_credentials.json'

# Set the delay between each mailbox check (e.g., 60 seconds)
CHECK_INTERVAL = 1

def process_email_content(email_body):
    # Placeholder for processing with OpenAI API
    summarized_content = email_body  # Replace with actual call to OpenAI API
    return summarized_content

def send_to_whatsapp(summarized_content):
    print("Sending to WhatsApp:", summarized_content)  # Replace with actual API call

def main():
    # Authenticate and create the Gmail API service
    service = authenticate_gmail_api(CREDENTIALS_PATH)

    # Get the most recent history ID
    profile = service.users().getProfile(userId='me').execute()
    history_id = profile.get('historyId')

    while True:
        # Fetch new messages since the last saved historyId
        new_messages = list_new_messages(service, history_id=history_id)

        # Process each new message
        for message_id in new_messages:
            details = get_message_details(service, 'me', message_id)
            if details:
                # Save the email content to a .txt file
                filename = f"email_{message_id}.txt"
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"From: {details['sender']}\n")
                    file.write(f"Subject: {details['subject']}\n")
                    file.write(f"Body:\n{details['body']}\n")
                
                # Optionally, mark the message as read
                mark_message_as_read(service, 'me', message_id)
                
        # Update the historyId for the next check
        profile = service.users().getProfile(userId='me').execute()
        history_id = profile.get('historyId')

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
