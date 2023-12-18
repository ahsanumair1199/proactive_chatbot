from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Conversation
from accounts.models import WhatsappUser
from twilio.rest import Client
import openai
from openai import OpenAI
import os

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


@api_view(['POST'])
def whatsapp_user_response(request):
    data = request.data
    whatsapp_number = data['From']
    whatsapp_number = whatsapp_number.split(':')[1]
    whatsapp_user = WhatsappUser.objects.get(phone_number=whatsapp_number)
    conversation = Conversation.objects.create(
        whatsapp_user=whatsapp_user,
        sender=whatsapp_number,
        receiver=data['To'].split(':')[1],
        text=data['Body'],
    )
    conversation.save()
    return Response("ok")
