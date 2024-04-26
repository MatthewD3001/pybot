
import discord
from discord.ext import commands
import database as db
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = ">", intents = intents)


class ConfirmLeave(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None

    @discord.ui.button(label = "Leave", style = discord.ButtonStyle.red)
    async def confirm(self, interaction, button):
        button.label = "Left"
        button.disabled = True
        self.value = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label = "Stay", style = discord.ButtonStyle.green)
    async def cancel(self, interaction, button):
        button.label = "Stayed"
        button.disabled = True
        self.value = False
        await interaction.response.edit_message(view=self)
        self.stop()


@bot.event
async def on_ready():
    print("\n-------------------------")
    print(f"Logged in as {bot.user}")
    print("-------------------------\n")
    db.init_db()


@bot.command()
async def join(ctx):
    user = ctx.author
    if db.in_db(user.id):
        if db.get_in_swap(user.id):
            await ctx.send(f"You're already in swap, {user.name}!")
        elif db.is_banned(user.id):
            await ctx.send(f"Sorry, you've been banned, {user.name} :(")
        else:
            db.set_in_swap(user.id, 1)
            await ctx.send(f"Welcome back, {user.name}!")
    else:
        db.add_user(user.id)
        await ctx.send(f"Thanks for joining swap, {user.name}!")


@bot.command()
async def leave(ctx):
    user = ctx.author
    if db.in_db(user.id):
        if db.is_banned(user.id):
            await ctx.send(f"You've already left swap due to being banned.")
        else:
            view = ConfirmLeave()
            await ctx.send(f"Are you sure that you want to leave, {user.name}?\nRemember, if swap has started then leaving will result in you being banned from the next swap.", view=view)
            
            await view.wait()
            if view.value is None:
                await ctx.send("The interaction timed out, nothing was performed, please redo your command if you wish to try again.")
                return
            elif view.value is True:
                db.leave_swap(user.id)
                await ctx.send(f"You have left the swap, we'll miss you, {user.name}!")
            else:
                await ctx.send(f"Thanks for choosing to stay, {user.name}! <3")

    else:
        await ctx.send(f"You're not in swap! You should reconsider and join instead, {user.name}!")


@bot.command()
async def letter(ctx, *, msg: str=''):
    user = ctx.author
    if db.in_db(user.id):
        letter = db.get_letter(user.id)
        if len(msg) < 1:
            if len(letter) > 0:
                await ctx.send(f"## Your letter:\n{letter}")
            else:
                await ctx.send("You do not have a letter yet.")
        else:
            db.edit_letter(user.id, msg)
            letter = db.get_letter(user.id)
            await ctx.send(f"## Your letter:\n{letter}")
    else:
        await ctx.send("You're not in the swap yet, do `>join` to join!")


@bot.command()
async def read(ctx):
    if db.swap_started():
        giftee_id: int = db.get_giftee(ctx.author.id)
        await ctx.send(f"Your giftee is\n## {giftee_id}\nHere's their letter:")
        await ctx.send(f"Dear Santa,\n\n{db.get_letter(giftee_id)}\n\nLove, {giftee_id}")
    else:
        await ctx.send("Swap hasn't started yet!!")


@bot.command()
async def butatime(ctx):
    await ctx.send(f"Right now it is {datetime.now().strftime('%H:%M:%S')} for buta.")

@bot.command()
async def ryuu(ctx):
    await ctx.send("<:umu:1232366655535972362>")


#############################
#                           #
#       ADMIN COMMANDS      #
#                           #
#############################
@bot.command()
async def sd(ctx):
    if ctx.author.id == 369982786356117504:
        await ctx.send("Shutting down...")
        db.close_db()
        await bot.close()
    else:
        await ctx.send("You're no admin!! :bonk:")


@bot.command()
async def ban(ctx, user_id: int):
    if ctx.author.id == 369982786356117504:
        db.set_ban(user_id, 1)
        await ctx.send(f"Banned user: {user_id}")
    else:
        await ctx.send("You're no admin!! :bonk:")


@bot.command()
async def start(ctx):
    if ctx.author.id == 369982786356117504:
        db.start_swap()
    else:
        await ctx.send("You're no admin!! :bonk:")


@bot.command()
async def list_swap(ctx):
    if ctx.author.id == 369982786356117504:
        santa_ids = db.get_user_ids_in_swap()
        output = "## Users in this swap:\n"
        first_id = santa_ids.pop()
        id = first_id
        for _ in range(len(santa_ids) + 1):
            user = bot.get_user(id)
            if user != None:
                output += str(user.name) + " -> "
            else:
                output += str(id) + " -> "
            id = db.get_giftee(id)

        user = bot.get_user(first_id)
        if user != None:
            output += str(user.name)
        else:
            output += str(first_id)
        await ctx.send(output)
    else:
        await ctx.send("You're no admin!! :bonk:")


@bot.command()
async def debug(ctx):
    if ctx.author.id == 369982786356117504:
        db.list_users()
    else:
        await ctx.send("You're no admin!! :bonk:")


file = open("../../pass/bottoken.txt", "r")
token = file.read()
file.close()
bot.run(token)
