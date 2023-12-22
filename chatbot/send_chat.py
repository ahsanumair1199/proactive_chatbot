from twilio.rest import Client
import openai
from openai import OpenAI
import os
from accounts.models import WhatsappUser
from .models import AddMessage, Conversation
from .helper_func import send_whatsapp_message, gen_embeddings


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_chat():
    print("Scheduler Called..")
    try:
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        openai_client = OpenAI()
        latest_message = AddMessage.objects.latest('-id')
        if latest_message.is_sent == False:
            whatsapp_users = WhatsappUser.objects.all()
            for whatsapp_user in whatsapp_users:
                media_urls = []
                if latest_message.image_url:
                    media_urls.append(latest_message.image_url)
                if latest_message.video_url:
                    media_urls.append(latest_message.video_url)
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=latest_message.message,
                    media_url=media_urls,
                    to=f'whatsapp:{whatsapp_user.phone_number}'
                )
                # conversation
                embedding = gen_embeddings(
                    openai_client, latest_message.message)
                conversation = Conversation.objects.create(
                    whatsapp_user=whatsapp_user,
                    sender='chatbot',
                    receiver=whatsapp_user.phone_number,
                    text=latest_message.message,
                    embedding=embedding
                )
                conversation.save()

            latest_message.is_sent = True
            latest_message.save()
        else:
            whatsapp_users = WhatsappUser.objects.all()
            for whatsapp_user in whatsapp_users:
                last_conversation = Conversation.objects.filter(
                    whatsapp_user=whatsapp_user).latest('-id')
                if last_conversation:
                    if last_conversation.sender == 'chatbot':
                        openai.api_key = os.environ.get('OPENAI_API_KEY')
                        openai_client = OpenAI()
                        gpt_response = openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "assistant",
                                 "content": f"Given the context of the user's message, craft a new response that strikes up a lively and engaging conversation. Ensure you sprinkle in some emojis to keep the tone upbeat and relatable! Think of this as an opportunity to connect with the user and spark a meaningful dialogue.\nContext: {last_conversation.text}"},
                            ]
                        )
                        gpt_answer = gpt_response.choices[0].message.content
                        send_whatsapp_message(client, '+14155238886',
                                              whatsapp_user.phone_number, gpt_answer)
                        embedding = gen_embeddings(
                            openai_client, gpt_answer)
                        conversation = Conversation.objects.create(
                            whatsapp_user=whatsapp_user,
                            sender='chatbot',
                            receiver=whatsapp_user.phone_number,
                            text=gpt_answer,
                            embedding=embedding
                        )
                        conversation.save()

    except AddMessage.DoesNotExist:
        pass
