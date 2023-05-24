# XnonBot Version 0.3.5
# Migrated from interactions.py to py-cord (hopefully it's a lot more stable!)
import discord
import random
from dotenv import load_dotenv
import os
from XnonBotModules import bot_req, keep_alive
import html

load_dotenv("C:\Programming\XnonBot\dev.env")
TOKEN = os.getenv("XNONBOTTOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix=";", intents=intents)

# Creating an instance of several subcommand groups that we'll use later.
game = bot.create_group("game")
generate = bot.create_group("generate")
utility = bot.create_group("utility")

COMMANDS = """
List of available commands:

`help` - Send a list of available slash commands
`github` - Send the GitHub page for this bot
`hello` - Say "Hello!"
`about` - Send information about the bot, such as its purpose and features
`inspire` - Send a random inspirational quote to uplift the user
`roll` - Send a random dice roll result, from 1 to 6
`rps` - Play rock, paper, scissors with the user
`say` - Tell the bot to say something (the same message you're inputting with the commmand)
`cat` - Send a random cat picture
`dog` - Send a random dog picture
`waifu` - Send a random waifu picture (it's SFW!)
`pexels` - Search an image on pexels.com
`trivia` - Send a random  trivia question and asking the user whether it's true or false
`convertticks` - Convert ticks to seconds
`convertseconds` - Convert seconds to ticks
`latency` - Check the bot's latency

Several commands are grouped into several command subgroups as of 24/05/2023 (update 0.3.5).
"""


"""Class for /trivia minigame"""


class TriviaButtons(discord.ui.View):
    @discord.ui.button(
        label="True",
        style=discord.ButtonStyle.primary,
        emoji="✅",
    )
    async def trivia_button_true_callback(self, button, interaction):
        if (
            interaction.user != interaction.message.author
        ):  # Check if the user pressing the button is the same one as the author.
            await interaction.response.send_message(
                "I wasn't asking you! To run another question, please send /trivia.",
                ephemeral=True,
            )
            return
        for child in self.children:
            child.disabled = True
            child.label = "Button disabled, no more pressing!"
        await interaction.response.edit_message(view=self)

        if correct_trivia_answer.lower() == "true":
            await interaction.followup.send(
                f"{interaction.user.mention} chooses True, {interaction.user.mention} is correct!"  # We're using followup.send() because we can't have interaction.response twice inside of the same function.
            )
        else:
            await interaction.followup.send(
                f"Sorry {interaction.user.mention}, but the answer is {correct_trivia_answer}."
            )

    @discord.ui.button(
        label="False",
        style=discord.ButtonStyle.danger,
        emoji="🚫",
    )
    async def trivia_button_false_callback(self, button, interaction):
        if interaction.user != interaction.message.author:
            await interaction.response.send_message(
                "I wasn't asking you! To run another question, please send /trivia.",
                ephemeral=True,
            )
            return
        for child in self.children:
            child.disabled = True
            child.label = "Button disabled, no more pressing!"
        await interaction.response.edit_message(view=self)

        if correct_trivia_answer.lower() == "false":
            await interaction.followup.send(
                f"{interaction.user.mention} chooses False, {interaction.user.mention} is correct!"
            )
        else:
            await interaction.followup.send(
                f"Sorry {interaction.user.mention}, but the answer is {correct_trivia_answer}."
            )


"""General subcommand group"""


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")


@bot.command(description="Say hello to the user.")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.user.mention}!")


@bot.command(description="Send a list of available slash commands.")
async def help(ctx):
    await ctx.respond(COMMANDS)


@bot.slash_command(description="Tell the bot to say something.")
async def say(ctx, message: discord.Option(str, description="Message to send.")):
    await ctx.respond(f"{ctx.user.mention} said: `{message}`")


@bot.command(description="Send the information about this bot.")
async def about(ctx):
    await ctx.respond(
        "I'm a chat-bot developed by XnonXte! My code is available on GitHub (/github)."
    )


@bot.command(description="Choose a random dice roll (1 to 6).")
async def roll(ctx):
    await ctx.respond(random.randint(1, 6))


@bot.command(description="Official GitHub page for this bot.")
async def github(ctx):
    await ctx.respond("https://github.com/XnonXte/XnonBot")


"""Generate subcommand group"""


@generate.command(description="Get a random quote from zenquotes.io")
async def quote(ctx):
    quote = bot_req.get_quote()
    await ctx.respond(quote)


@generate.command(
    description="Get a random waifu picture from https://waifu.pics/docs (It's SFW!)"
)
async def waifu(
    ctx,
    category: discord.Option(
        str,
        description="Select the category (e.g. waifu, please refer to https://waifu.pics/docs for more categories!)",
    ),
):
    waifu_pic = bot_req.get_waifu_pic(category)
    if waifu_pic is None:
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return
    await ctx.respond(waifu_pic)


@generate.command(description="Get a random dog picture from https://dog.ceo/dog-api")
async def dog(ctx):
    dog = bot_req.get_dog_pic()
    await ctx.respond(dog)


@generate.command(description="Get a random cat picture from https://thecatapi.com")
async def cat(ctx):
    cat = bot_req.get_cat_pic()
    await ctx.respond(cat)


@generate.command(description="Search an image on pexels.com")
async def pexels(
    ctx, search_query: discord.Option(str, description="Image to search.")
):
    try:
        image_output = bot_req.get_pexels_photos(search_query)
        await ctx.respond(
            f"Here's a(n) {search_query} image for you! {image_output[2]}"
        )
    except Exception as e:
        await ctx.respond(f"An error has been encountered: {e}", ephemeral=True)


"""Utility subcommand group"""


@utility.command(description="Check the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! My ping is {round(bot.latency * 100, 2)}ms.")


@utility.command(description="Convert ticks to seconds.")
async def convertticks(
    ctx, value: discord.Option(str, description="Enter the value in ticks.")
):
    convert = value * 0.015
    await ctx.respond(f"{value} ticks is equal to {convert} seconds.")


@utility.command(description="Convert seconds to ticks.")
async def convertseconds(
    ctx, value: discord.Option(float, description="Enter the value in seconds.")
):
    convert = value / 0.015
    await ctx.respond(f"{value} seconds is equal to {int(convert)} ticks.")


"""Game subcommand group"""


@game.command(description="Play rock, paper, scissors with the user.")
async def rps(
    ctx,
    choice: discord.Option(str, description="Choose either rock, paper, or scissors."),
):
    choices = ("rock", "paper", "scissors")
    bot_choice = random.choice(choices)

    if choice not in choices:
        await ctx.respond(
            "Invalid choice. Please choose either rock, paper, or scissors!",
            ephemeral=True,
        )
        return

    if choice == bot_choice:
        await ctx.respond(
            f"{ctx.user.mention} chooses {choice}. I choose {bot_choice}. We tied!"
        )
    elif choice == "rock" and bot_choice == "scissors":
        await ctx.respond(
            f"{ctx.user.mention} chooses {choice}. I choose {bot_choice}. {ctx.user.mention} won!"
        )
    elif choice == "scissors" and bot_choice == "paper":
        await ctx.respond(
            f"{ctx.user.mention} chooses {choice}. I choose {bot_choice}. {ctx.user.mention} won!"
        )
    elif choice == "paper" and bot_choice == "rock":
        await ctx.respond(
            f"{ctx.user.mention} chooses {choice}. I choose {bot_choice}. {ctx.user.mention} won!"
        )
    else:
        await ctx.respond(
            f"{ctx.user.mention} chooses {choice}. I choose {bot_choice}. I won!"
        )


@game.command(description="Play a trivia game from https://opentdb.com/")
async def trivia(
    ctx,
    category: discord.Option(
        str,
        description="Choose the category (e.g. animal, refer to the GitHub page for more categories)",
    ),
):
    global correct_trivia_answer
    trivia_question = bot_req.get_trivia(category.lower())
    if trivia_question is None:
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return
    correct_trivia_answer = trivia_question[2]

    await ctx.respond(
        html.unescape(f"The difficulty is {trivia_question[1]} - {trivia_question[0]}")
    )

    await ctx.respond(
        f"Please select your answer down below (In under 10 seconds!)",
        view=TriviaButtons(),
    )


"""Context menus"""


@bot.user_command(name="Creation date")
async def creation_date(ctx, member: discord.Member):
    await ctx.respond(
        f"The account {member.name} was created at `{member.created_at}`."
    )


@bot.user_command(name="Join date")
async def join_date(ctx, member: discord.Member):
    await ctx.respond(f"The account {member.name} joined at `{member.joined_at}`.")


# Keeping the bot alive and running the bot.
# keep_alive.keep_alive()
bot.run(TOKEN)
