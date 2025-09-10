import token
from xml.sax import handler
from src.langchain_helper import *
from src.discord_helper import *
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import logging
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
    bot = bot_set_up()
    bot.run(token=token, log_handler=handler)



if __name__ == "__main__":
    main()  