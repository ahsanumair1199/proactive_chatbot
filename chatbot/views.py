from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Conversation, GptResponse
from accounts.models import WhatsappUser
from twilio.rest import Client
import openai
from openai import OpenAI
import os
from pgvector.django import L2Distance
from .helper_func import send_whatsapp_message, gpt_text_gen, gen_embeddings

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


@api_view(['POST'])
def whatsapp_user_response(request):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai_client = OpenAI()
    data = request.data
    user_chat_emb = gen_embeddings(openai_client, data['Body'])
    whatsapp_number = data['From']
    whatsapp_number = whatsapp_number.split(':')[1]
    whatsapp_user = WhatsappUser.objects.get(phone_number=whatsapp_number)

    # check similarity in conversation
    user_conversation = Conversation.objects.filter(whatsapp_user=whatsapp_user).annotate(
        distance=L2Distance('embedding', user_chat_emb)
    ).order_by('distance').first()
    if user_conversation and user_conversation.distance < 0.3:
        print(user_conversation.distance)
        gpt_response = GptResponse.objects.get(conversation=user_conversation)
        send_whatsapp_message(client, '+14155238886',
                              whatsapp_number, gpt_response.text)
    else:
        conversation = Conversation.objects.create(
            whatsapp_user=whatsapp_user,
            sender=whatsapp_number,
            receiver=data['To'].split(':')[1],
            text=data['Body'],
            embedding=user_chat_emb
        )
        conversation.save()

        # chatgpt
        gpt_answer = gpt_text_gen(openai_client, data)
        send_whatsapp_message(client, '+14155238886',
                              whatsapp_number, gpt_answer)
        gpt_answer_emb = gen_embeddings(openai_client, gpt_answer)
        gpt_response = GptResponse.objects.create(
            whatsapp_user=whatsapp_user,
            conversation=conversation,
            text=gpt_answer,
            embedding=gpt_answer_emb
        )
        gpt_response.save()
    return Response("ok")
