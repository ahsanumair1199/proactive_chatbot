from twilio.rest import Client
import os
from accounts.models import WhatsappUser
from .models import AddMessage


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_chat():
    print("Send Chat Called..")
    latest_message = AddMessage.objects.latest('-id')
    whatsapp_users = WhatsappUser.objects.all()
    if latest_message.is_sent == False:
        for whatsapp_user in whatsapp_users:
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=latest_message.message,
                to=f'whatsapp:{whatsapp_user.phone_number}'
            )
        latest_message.is_sent = True
        latest_message.save()
