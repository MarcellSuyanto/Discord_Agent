import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import logging
from dotenv import load_dotenv
import os
from src.langchain_helper import ask_text, search_text
from src.whisper_stt import *
import asyncio

def bot_set_up():
    intents = discord.Intents.default()

    intents.message_content = True
    intents.members = True
    intents.presences = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    #Checks when the bot is online
    @bot.event
    async def on_ready():
        print(f"I am {bot.user.name}")

    voice_tasks = {}
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

        task = voice_tasks.get(ctx.guild.id)
        print(task)
        if task and not task.done():
            await ctx.send("[DEBUG] Voice recognition already running for this server.")
        else:
            await ctx.send("Hello")
            voice_tasks[ctx.guild.id] = asyncio.create_task(startVoiceInput(ctx))
            print(voice_tasks)

    @bot.command(name="ask")
    @commands.guild_only()
    async def ask(ctx, *, question:str)-> None:
        author = ctx.author
        async with ctx.typing():
            response = ask_text(question)
        await ctx.send(f"{author.mention}, {response}")

    @bot.command(name="search")
    @commands.guild_only()
    async def search(ctx, *, query:str)-> None:
        author = ctx.author
        async with ctx.typing():
            response = search_text(query)
        await ctx.send(f"{author.mention}, {response}")
    
    return bot


