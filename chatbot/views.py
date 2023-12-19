from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Conversation, GptResponse
from accounts.models import WhatsappUser
from twilio.rest import Client
import openai
from openai import OpenAI
import os
from pgvector.django import L2Distance

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


@api_view(['POST'])
def whatsapp_user_response(request):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai_client = OpenAI()
    data = request.data
    response = openai_client.embeddings.create(
        input=data['Body'],
        model="text-embedding-ada-002"
    )
    whatsapp_number = data['From']
    whatsapp_number = whatsapp_number.split(':')[1]
    whatsapp_user = WhatsappUser.objects.get(phone_number=whatsapp_number)
    conversation = Conversation.objects.create(
        whatsapp_user=whatsapp_user,
        sender=whatsapp_number,
        receiver=data['To'].split(':')[1],
        text=data['Body'],
        embedding=response.data[0].embedding
    )
    conversation.save()

    # chatgpt
    gpt_responses = GptResponse.objects.filter(
        whatsapp_user=whatsapp_user).order_by()
    if gpt_responses:
        for gpt_response in gpt_responses:
            print(gpt_response.text)
    else:
        model = "text-davinci-002"
        text_gen_response = openai_client.chat.completions.create(
            engine=model,
            prompt=data['Body'],
            max_tokens=150
        )
        print(text_gen_response.choices[0].message.content)
        gpt_emb_response = openai_client.embeddings.create(
            input=response.choices[0].message.content,
            model="text-embedding-ada-002"
        )
        gpt_response = GptResponse.objects.create(
            whatsapp_user=whatsapp_user,
            text=response.choices[0].message.content,
            embedding=gpt_emb_response.data[0].embedding
        )
        gpt_response.save()
    return Response("ok")
