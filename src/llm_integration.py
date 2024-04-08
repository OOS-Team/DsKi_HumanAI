import requests
import time
import os

def send_to_llm(email_content, config):
    """
    Sendet den Inhalt der E-Mail an das lokale LLM zur Verarbeitung.

    Args:
        email_content: Der zu verarbeitende E-Mail-Text.
        config: Konfiguration für die Verbindung mit dem LLM, einschließlich base_url und eventuell API-Schlüssel.

    Returns:
        Die Antwort des LLM, typischerweise verarbeiteter Text oder eine Zusammenfassung.
    """
    try:
        response = requests.post(
            f"{config['base_url']}/v1/engines/mistral-7b/completions",
            headers={'Authorization': f"Bearer {config['api_key']}"} if config['api_key'] != "NULL" else {},
            json={
                'prompt': email_content,
                'temperature': 0.5,
                'max_tokens': 150,
                'top_p': 1,
                'frequency_penalty': 0,
                'presence_penalty': 0
            }
        )
        response.raise_for_status()  # Löst eine Ausnahme aus, wenn der HTTP-Statuscode ein Fehler ist.
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred when contacting the LLM: {e}")
        return None

def save_llm_response(response, storage_path='emails/gpt_response'):
    """
    Speichert die Antwort des LLM in einer Datei.

    Args:
        response: Die vom LLM erhaltene Antwort.
        storage_path: Der Pfad, unter dem die Antwort gespeichert werden soll.

    Returns:
        Der Dateiname der gespeicherten Antwort.
    """
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    filename = os.path.join(storage_path, f"llm_response_{time.strftime('%Y%m%d-%H%M%S')}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        # Sicherstellen, dass die Antwort das erwartete Format hat
        if response and 'choices' in response and len(response['choices']) > 0:
            file.write(response['choices'][0]['text'])
        else:
            file.write("No response or unexpected format received from LLM.")
    return filename
