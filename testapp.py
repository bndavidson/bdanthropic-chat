import os
# from dotenv import load_dotenv
import chainlit as cl

print('key test 2')


@cl.on_chat_start
async def start_chat():
    cl.user_session.set("messages", [])


