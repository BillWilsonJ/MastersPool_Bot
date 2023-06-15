# main.py
import os
import live_scores

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Stat Bot
class ServerUser:

    def __init__(self, n):
        self.name = n
        self.num_of_messages = 1
        self.channels = []

    def incrementMessageCount(self):
        self.num_of_messages = self.num_of_messages + 1

    def addChannel(self,channel_name):
        self.channels.append(channel_name)

class ChannelInformation:

    def __init__(self, n):
        self.name = n
        self.num_of_messages = 1

    def incrementMessageCount(self):
        self.num_of_messages = self.num_of_messages + 1

# !Stat Bot

intents = discord.Intents().all()
client = discord.Client(intents=intents)

# Stat Bot

serverUsers = []
serverusersNames = []
channelInformations = []

# !Stat Bot

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')

# Stat Bot 
"""""
    for server in client.guilds:
        for channel in server.channels:
            if str(channel.type) == 'text':
                print(channel.name)
                channelInformations.append(ChannelInformation(channel.name))
                async for msg in channel.history(limit=100000):
                    if str(msg.author.name) in serverusersNames:
                        serverusersNames.append(msg.author.name)
                        for server_user in serverUsers:
                            if str(msg.author.name) == server_user.name:
                                server_user.incrementMessageCount()
                    else:
                        serverUsers.append(ServerUser(msg.author.name))
                        serverusersNames.append(msg.author.name)

                    for channelinfo in channelInformations:
                        if str(channel.name) == channelinfo.name:
                            channelinfo.incrementMessageCount()

    serverUsers.sort(key=lambda x: x.num_of_messages)
    channelInformations.sort(key=lambda x: x.num_of_messages)

    for server_user in serverUsers:
        print(server_user.name + " has said " + str(server_user.num_of_messages) + " messages")
    for channelinfo in channelInformations:
        print(channelinfo.name + " has  " + str(server_user.num_of_messages) + " messages")
"""""
# !Stat Bot

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Test"):
        await message.channel.send("Message sent in " + message.channel.name + " channel")

    if message.channel.name == "golf-major-pools" or message.channel.name == "bot-test":
        if message.content.startswith("!"):
            if message.content.startswith("!Leaderboard") or message.content.startswith("!leaderboard") or message.content.startswith("!lb"):
                leaderboard_output = ""
                leaderboard_output = live_scores.get_leaderboard()
                await message.channel.send(leaderboard_output)
            elif message.content.startswith("!Tiger"):
                await message.channel.send("get lost loser")
            else:
                name = message.content.replace('!','')
                score_output = live_scores.users_scores(name)
                await message.channel.send(score_output)

client.run(TOKEN)