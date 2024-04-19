# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import database as db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '>', intents = intents)

@bot.event
async def on_ready():
    print('\n-------------------------')
    print(f'Logged in as {bot.user}')
    print('-------------------------\n')

    db.init_db()

@bot.command()
async def join(ctx):
    user = ctx.author
    if db.in_db(user.id):
        if db.get_in_swap(user.id):
            await ctx.send(f'You\'re already in swap, {user.name}!')
        elif db.is_banned(user.id):
            await ctx.send(f'Sorry, you\'ve been banned, {user.name} :(')
        else:
            db.set_in_swap(user.id, 1)
            await ctx.send(f'Welcome back, {user.name}!')
    else:
        db.add_user(user.id)
        await ctx.send(f'Thanks for joining swap, {user.name}!')


@bot.command()
async def leave(ctx):
    user = ctx.author
    if db.in_db(user.id):
        if db.is_banned(user.id):
            await ctx.send(f'You\'ve already left swap due to being banned.')
        else:
            db.set_in_swap(user.id, 0)
            await ctx.send(f'You have left the swap, we\'ll miss you, {user.name}!')
    else:
        await ctx.send(f'You\'re not in swap! You should reconsider and join instead, {user.name}!')

@bot.command()
async def letter(ctx, *, msg: str=''):
    user = ctx.author
    if db.in_db(user.id):
        letter = db.get_letter(user.id)
        if len(msg) < 1:
            if len(letter) > 0:
                await ctx.send(f'Your letter:\n{letter}')
            else:
                await ctx.send('You do not have a letter yet.')
        else:
            db.edit_letter(user.id, msg)
            letter = db.get_letter(user.id)
            await ctx.send(f'Your letter:\n{letter}')
    else:
        await ctx.send('You\'re not in the swap yet, do `>join` to join!')


@bot.command()
async def ryuu(ctx):
    await ctx.send(':umu:')


#############################
#                           #
#       ADMIN COMMANDS      #
#                           #
#############################
@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 369982786356117504:
        await ctx.send('Shutting down...')
        db.close_db()
        await bot.close()
    else:
        await ctx.send('You\'re no admin!! :bonk:')


@bot.command()
async def ban(ctx, user_id: int):
    if ctx.author.id == 369982786356117504:
        db.set_ban(user_id, 1)
        await ctx.send(f'Banned user: {user_id}')
    else:
        await ctx.send('You\'re no admin!! :bonk:')


@bot.command()
async def start(ctx):
    if ctx.author.id == 369982786356117504:
        db.start_swap()
    else:
        await ctx.send('You\'re no admin!! :bonk:')


@bot.command()
async def list_swap(ctx):
    if ctx.author.id == 369982786356117504:
        giftee_ids = db.get_user_ids_in_swap()
        output = "## Users in this swap:\n"
        cur_id = giftee_ids[0]
        for i in range(len(giftee_ids)):
            user = bot.get_user(cur_id)
            if user != None:
                output += str(user.name) + " -> "
            else:
                output += str(cur_id) + " -> "
            cur_id = db.get_giftee(cur_id)
        output += str(giftee_ids[0])
        await ctx.send(output)
    else:
        await ctx.send('You\'re no admin!! :bonk:')


file = open("../../pass/bottoken.txt", "r")
token = file.read()
file.close()
bot.run(token)
