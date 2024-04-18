# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import database as db

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '>', intents = intents)

@bot.event
async def on_ready():
    print('\n-------------------------')
    print(f'Logged in as {bot.user}')
    print('-------------------------\n')

    db.init_db()

@bot.command()
async def letter(ctx, *, msg: str=''):
    await ctx.send(f'Writing letter for {ctx.author.id} which contains: {msg}')
    user_id = ctx.author.id
    if db.in_db(user_id):
        letter = db.get_letter(user_id)
        if len(letter) > 0:
            await ctx.send(f'Your letter:\n\n{letter}')
        else:
            await ctx.send('Edit letter')
    else:
        db.add_user(user_id, msg)

    db.list_users()

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 369982786356117504:
        await ctx.send('Shutting down...')
        await bot.close()
    else:
        await ctx.send('You\'re no admin!! :bonk:')

file = open("../../pass/bottoken.txt", "r")
token = file.read()
file.close()
bot.run(token)
