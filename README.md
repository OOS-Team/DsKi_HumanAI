# LLM Email Ranking

Dieses Projekt leitet E-Mails von einem Gmail-Konto über die OpenAI-API zur Zusammenfassung an eine WhatsApp-Nummer weiter. Es nutzt die Gmail API, um auf neue E-Mails zuzugreifen, verwendet die OpenAI-API, um den Inhalt zu analysieren und zu verdichten, und sendet die zusammengefassten Informationen über die WhatsApp-API.

## Projekt Setup

Folgen Sie diesen Schritten, um die Entwicklungsumgebung einzurichten und das Projekt zu starten.

### Voraussetzungen

- Python 3.8 oder höher
- Pip (Python-Paketmanager)
- Ein Google Cloud Platform (GCP) Konto
- Ein OpenAI API-Schlüssel
- Zugriff auf WhatsApp-APIs (z.B. über Twilio)

### Umgebung Einrichten

1. **Virtuelle Umgebung erstellen (optional, aber empfohlen):**

   ```bash
   python3 -m venv venv
   ```

2. **Virtuelle Umgebung aktivieren:**

   - Für Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - Für Unix oder MacOS:

     ```bash
     source venv/bin/activate
     ```

3. **Abhängigkeiten installieren:**

   Installieren Sie die erforderlichen Python-Pakete über pip:

   ```bash
   pip install -r requirements.txt
   ```

### Gmail API Credentials & Token Setup

1. **GCP Projekt erstellen:**

   Besuchen Sie die [Google Cloud Console](https://console.cloud.google.com/), erstellen Sie ein neues Projekt und merken Sie sich die Projekt-ID.

2. **Gmail API aktivieren:**

   Suchen Sie in der Bibliothek der Google Cloud Console nach der Gmail API und aktivieren Sie sie für Ihr Projekt.

3. **OAuth 2.0-Client-IDs erstellen:**

   - Navigieren Sie zu "Anmeldeinformationen" und erstellen Sie Anmeldeinformationen vom Typ "OAuth 2.0-Client-IDs".
   - Konfigurieren Sie das OAuth-Zustimmungsbildschirm.
   - Laden Sie die JSON-Datei mit Ihren Anmeldeinformationen herunter und speichern Sie sie als `credentials.json` im Projektverzeichnis.

4. **Token generieren:**

   Führen Sie Ihr Projekt das erste Mal aus. Der Authentifizierungsprozess öffnet einen Browser, in dem Sie sich anmelden und den Zugriff auf Ihr Gmail-Konto gewähren müssen. Nach erfolgreicher Authentifizierung wird ein Token gespeichert, das für zukünftige Anfragen verwendet wird.

## Projektzusammenfassung

Das Projekt implementiert eine durchgehende Lösung, die folgende Schritte umfasst:

1. **Gmail-API-Zugriff:** Das Skript überwacht kontinuierlich ein Gmail-Konto auf neue E-Mails.
2. **Inhaltsanalyse:** E-Mails werden über die OpenAI-API gesendet, um eine Zusammenfassung des Inhalts zu erstellen.
3. **Weiterleitung an WhatsApp:** Die zusammengefassten Inhalte werden anschließend über eine WhatsApp-API an eine vorgegebene Nummer gesendet.

Dies ermöglicht eine effiziente Informationsweitergabe und stellt sicher, dass wichtige E-Mail-Inhalte schnell und bequem über WhatsApp geteilt werden können.
```