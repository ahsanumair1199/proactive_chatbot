# Description
A Django based project which contains the APIs to handle the Twilio and whatsapp communication. Users can chat with the chatbot via their whatsapp.
# Setup

Install required libraries

```bash
pip install -r requirements.txt
```

# Run the Server

```bash
python manage.py runserver
```

# Ngrok

Run the Ngrok tunnel on port 8000. Replace Ngrok server url in Twilio sandbox settings. It will capture the whatsapp user messages and transfer it to the backend server.

# Admin Panel

127.0.0.1:8000/admin
