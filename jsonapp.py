import chainlit as cl
import os
import base64
# from dotenv import load_dotenv
import anthropic

import requests
import json

print('URL test')
url = "https://api.www.sbir.gov/public/api/solicitations?agency=HHS"

my_api_key = os.getenv("ANTHROPIC_API_KEY")


def get_json_from_url(url):
    """
    Fetch json data from a URL and optionally save it to a file.
    Returns: dict or list: Parsed JSON data from the URL.
    """
    try:
        # Fetch data from URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON
        data = response.json()

        print(f"Successfully fetched data from {url}")
        return data

    except requests.exceptions.RequestExcepton as e:
        print(f"Error fetching data: {e}")
        return None


    
c = anthropic.AsyncAnthropic(api_key=my_api_key)

@cl.on_chat_start
async def start():

    # print the url
    await cl.Message(
      content=url
    ).send()

    rfp = get_json_from_url(url)
    rfptext = json.dumps(rfp, indent=2)

    print(rfptext)
    
    printmessage='FUCK YA'
    await cl.Message(
        content=f"You said: {printmessage}"
    ).send()
       

    cl.user_session.set("messages", [])
    messages = cl.user_session.get("messages")

    print("Sending something to Claude...")
    # messages = []
    # messages.append({"role": "user", "content": "hello claude. are you there? My name is Brian. What is my name?"})
    # messages.append({"role": "user", "content": message_content})
    messages.append({"role":"user", "content": f"Describe the following JSON object:\n\n{rfptext}"})


    # response = await c.messages.create(
    # model="claude-3-5-sonnet-latest",
    # messages=messages,
    # max_tokens=1000
    # )
        
    # response_text = response.content[0].text
    # print(response_text)
    
    # cl.user_session.set("messages", [])


async def call_claude(query: str):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": query})

    msg = cl.Message(content="", author="Claude")

    stream = await c.messages.create(
        model="claude-3-5-sonnet-latest",
        messages=messages,
        max_tokens=1000,
        stream=True
    )

    async for data in stream:
        if data.type == "content_block_delta":
            await msg.stream_token(data.delta.text)

    await msg.send()
    messages.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("messages", messages)

@cl.on_message
async def chat(message: cl.Message):
    await call_claude(message.content)




