import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

#Checks when the bot is online
@bot.event
async def on_ready():
    print(f"I am {bot.user.name}")

#Join VC
@bot.command(name="join")
@commands.guild_only()
async def join(ctx):
    author = ctx.author
    channel = author.voice.channel if author.voice else None
    if channel is None:
        return await ctx.send("You must be in a voice channel.")

    # If already connected in this guild, move instead of reconnecting
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_connected():
        await vc.move_to(channel)
    else:
        await channel.connect(self_deaf=False, self_mute=False)

    await ctx.send(f"Joined **{channel.name}**.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)