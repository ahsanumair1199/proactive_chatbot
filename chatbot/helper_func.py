def send_whatsapp_message(client, from_number, to_number, message_body):
    max_message_length = 1600

    # Split the message into chunks
    message_chunks = [message_body[i:i + max_message_length]
                      for i in range(0, len(message_body), max_message_length)]

    for index, message_chunk in enumerate(message_chunks, start=1):
        # Create a new message for each chunk
        message = client.messages.create(
            from_=f'whatsapp:{from_number}',
            body=message_chunk,
            to=f'whatsapp:{to_number}'
        )


def gpt_text_gen(openai_client, data):
    gpt_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"Answer the following in less than 1600 characters:\n{data['Body']}"},
        ]
    )
    gpt_answer = gpt_response.choices[0].message.content
    print(gpt_answer)
    return gpt_answer


def gen_embeddings(openai_client, input):
    response = openai_client.embeddings.create(
        input=input,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
