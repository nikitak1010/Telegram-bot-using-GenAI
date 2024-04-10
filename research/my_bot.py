from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import os
import logging
import openai

load_dotenv()
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

#connect with openai
openai.api_key = OPENAI_API_KEY

#print("OK")

MODEL_NAME = "gpt-3.5-turbo"

#Initialize bot
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()

def clear_past():
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def command_start_handler(message: types.Message):
    """This handler receives messages with `/start` or `/help` command
    Args:
        message (types.Message): __descriptions__
    """
    await message.reply("Hi!\n I am a MRSPTU College Bot. How can i assist you?")


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)