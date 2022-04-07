# main.py
import os
import live_scores

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Test"):
        await message.channel.send("Message sent in " + message.channel.name + " channel")

    if message.channel.name == "masters-pool-2022":
        if message.content.startswith("!"):
            if message.content.startswith("!Leaderboard"):
                leaderboard_output = ""
                leaderboard_output = live_scores.get_leaderboard()
                await message.channel.send(leaderboard_output)
            elif message.content.startswith("!Tiger"):
                await message.channel.send("Fuck off")
            else:
                name = message.content.replace('!','')
                score_output = live_scores.users_scores(name)
                await message.channel.send(score_output)

client.run(TOKEN)