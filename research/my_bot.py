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

#MODEL_NAME = "gpt-3.5-turbo"
MODEL_NAME = "davinci"

#Initialize bot
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()

def clear_past():
    reference.response = ""

@dispatcher.message_handler(commands=['clear'])
async def welcome(message: types.Message):
    """This handler to clear the previous conversation and context.
   
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context")


@dispatcher.message_handler(commands=['start','hi','hello','hlo'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or `/help` command
    Args:
        message (types.Message): __descriptions__
    """
    await message.reply("Hi!\n I am a MRSPTU College Bot. How can i assist you?")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to dispkay the help menu.
    """
    help_command ="""
    Hi, I am a bot created by Nikita Kansal! Please follow these commands -
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message_handler(commands=['about_mrsptu'])
async def about_mrsptu(message: types.Message):
    """
    A handler to display information of mrsptu.
    """
    info ="""
    Maharaja Ranjit Singh Punjab Technical University (MRSPTU), Bathinda (Erstwhile Maharaja Ranjit Singh State Technical University, Bathinda) is an affiliating Technical University, established by Govt. of Punjab vide Punjab Act No. 5 of 2015 notified through Punjab Government Gazette-Extraordinary (Regd. No. CHD/0092/2015-2017) notification No. 5- Leg./2015 dated 12th February 2015 and registered with UGC u/s 2(f).
With spontaneous upswing in demand for quality Technical Education, burgeoning pressure on the Premier Technical University of Punjab, Punjab Technical University, Kapurthala, to mitigate regional imbalance in distribution of Temples of quality Technical Education in the State, for exponential socio-economic growth of the Malwa region, to bridge the gap between demand and supply of employable technical human resource, exigency for creation of a new State Technical University in Punjab was realized. Consequent on the implementation of this Act, Technical institutions of eleven districts of Punjab have been affiliated to MRSPTU with effect of 1st July, 2015 including Barnala, Bathinda, Faridkot, Fatehgarh Sahib, Fazilka, Ferozepur, Mansa, Moga, Patiala, Sangrur and Sri Muktsar Sahib.
The objectives of this new Technical University at Bathinda are to provide, upgrade and promote Quality Technical Education, Training and Research in Technical Education to create entrepreneurship and a conducive environment for the pursuit of Technical Education in close cooperation with industry. In the pursuit of creating excellence in Teaching, Research and Skill Development, the University has to attain highest standards by following and conforming to norms/standards policies laid down by the All India Council for Technical Education, New Delhi and University Grants Commission, New Delhi.
As an outcome of the above endeavours, the University is expected to generate and maintain resources through consultancy services, testing services, Continuing Education Programmes, national and international collaborations, MoU, transfer of intellectual property rights, etc. MRSPTU will cater to the needs of Quality Technical Education in eleven districts of Punjab encompassed in its jurisdiction. New M.Tech. & Ph.D. Programmes are being initiated from 2016-17 academic sessions. New skill development certificate courses in 9 areas of Engineering in the Constituent Colleges of the University and four PG Certificate Courses in Pharmacy in Affiliated Colleges are also being planned.
    """
    await message.reply(info)
    
@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    #A handler to process the user's input and generate a response using the openai API.

    """
    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text=reference.response)
   

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)