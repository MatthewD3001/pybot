# This example requires the 'message_content' intent.

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith('>letter'):
        await message.channel.send('writing letter: ' + extract_content(msg))

    elif msg.startswith('>write-santa'):
        await message.channel.send('writing to santa: ' + extract_content(msg))

    elif msg.startswith('>write-giftee'):
        await message.channel.send('writing to giftee: ' + extract_content(msg))

    elif msg.startswith('>read'):
        await message.channel.send('reading!!!')

def extract_content(msg):
    for i in range(0, len(msg)):
        if msg[i] == ' ' or msg[i] == '\n':
            if msg[i + 1] == '\n':
                return msg[i + 2:]
            else:
                return msg[i + 1:]

file = open("../../pass/bottoken.txt", "r")
token = file.read()
file.close()
client.run(token)
