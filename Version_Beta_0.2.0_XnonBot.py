# XnonBot Version Beta 0.2
# New and improved XnonBot source code written in Python, currently using discord.py 2.2.3
# Utilizing discord.ext to use the Bot commands framework that discord has been integrating itself with

# Importing dependencies
import discord
import bot_req
import html
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\dev.env")
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

slash_command_dict = """
List of commands prompted using slash command: 

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
`waifu` - Send a random waifu picture (it's mostly SFW!)
`pexels` - Search an image on pexels.com
"""

command_dict = """
List of commands prompted using ("$")

`animaltrivia` - Send a random animal trivia and asking the user whether it's true or false
`mathtrivia` - Send a random math trivia and asking the user whether it's true or false
`animetrivia` - Send a random anime trivia and asking the user whether it's true or false
"""


# bot.event decorator
@bot.event
async def on_ready():
    print(f"The bot is running as {bot.user.name}")
    try:
        synced = await bot.tree.sync(
        )  # Syncs all available slash commands as it is a discord requirement
        print(f"{len(synced)} command(s) synced!")
    except Exception as e:
        print(e)


# bot.tree.command() decorator, we're using this instead of bot.command()
@bot.tree.command(name="hello", description="Say hello to the user.")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")


@bot.tree.command(name="help",
                  description="Send a list of available slash commands.")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(slash_command_dict)


@bot.tree.command(name="say", description="Tell the bot to say something.")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(
        f"{interaction.user.mention} said: `{thing_to_say}`")


@bot.tree.command(name="about",
                  description="Send the information about this bot.")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        "As the name implies, I'm a simple chatbot created by XnonXte!")


@bot.tree.command(name="roll",
                  description="Choose a random dice roll (1 from 6).")
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(random.randint(1, 6))


@bot.tree.command(name="github",
                  description="Send the github page for this bot.")
async def github(interaction: discord.Interaction):
    await interaction.response.send_message("https://github.com/XnonXte/XnonBot")


@bot.tree.command(name="quote",
                  description="Get a random quote.")
async def quote(interaction: discord.Interaction):
    quote = bot_req.get_quote()
    await interaction.response.send_message(quote)


@bot.tree.command(name="dog",
                  description="Get a random dog picture.")
async def dog(interaction: discord.Interaction):
    dog = bot_req.get_dog_pic()
    await interaction.response.send_message(dog)


@bot.tree.command(
    name="cat", description="Get a random cat picture.")
async def cat(interaction: discord.Interaction):
    cat = bot_req.get_cat_pic()
    await interaction.response.send_message(cat)


@bot.tree.command(
    name="waifu",
    description="Get a random waifu picture.")
async def waifu(interaction: discord.Interaction):
    waifu = bot_req.get_waifu_pic()
    await interaction.response.send_message(waifu)


@bot.tree.command(name="rps",
                  description="Play rock, paper, scissors with the bot.")
async def rps(interaction: discord.Interaction, choice: str):
    choices = ("rock", "paper", "scissors")
    bot_choice = random.choice(choices)

    if choice not in choices:
        await interaction.response.send_message(
            'Invalid choice. Please choose either rock, paper, or scissors!',
            ephemeral=True)
        return

    if choice == bot_choice:
        await interaction.response.send_message(
            f'{interaction.user.mention} chose {choice}. I chose {bot_choice}. We tied!'
        )
    elif choice == 'rock' and bot_choice == 'scissors':
        await interaction.response.send_message(
            f'{interaction.user.mention} chose {choice}. I chose {bot_choice}. {interaction.user.mention} won!'
        )
    elif choice == 'scissors' and bot_choice == 'paper':
        await interaction.response.send_message(
            f'{interaction.user.mention} chose {choice}. I chose {bot_choice}. {interaction.user.mention} won!'
        )
    elif choice == 'paper' and bot_choice == 'rock':
        await interaction.response.send_message(
            f'{interaction.user.mention} chose {choice}. I chose {bot_choice}. {interaction.user.mention} won!'
        )
    else:
        await interaction.response.send_message(
            f'{interaction.user.mention} chose {choice}. I chose {bot_choice}. I won!'
        )


@bot.tree.command(name="pexels", description="Search an image on pexels.com")
async def pexels(interaction: discord.Interaction, query: str):
    image_output = bot_req.get_pexels_photos(query)
    await interaction.response.send_message(
        f"An image of {query} has been generated! Photographed by: {image_output[0]}, original link: {image_output[2]} - Powered by pexels.com"
    )


@bot.event
async def on_message(message):

    def check_message(initial_requests):
        return initial_requests.author == message.author and initial_requests.channel == message.channel and initial_requests.content.lower(
        ) in ["true", "false"]

    if message.content.startswith("$help"):
        await message.channel.send(command_dict)

    if message.content.startswith("$animaltrivia"):
        animal_trivia = bot_req.get_animal_trivia()
        await message.channel.send(
            html.unescape(
                f"{animal_trivia[0]} True or false? The difficulty is {animal_trivia[1]}."
            ))

        response = await bot.wait_for("message", check=check_message)

        if response.content.lower() == animal_trivia[2].lower():
            await message.channel.send("You're correct!")
        else:
            await message.channel.send(
                f"Sorry, but the correct answer was {animal_trivia[2]}.")

    if message.content.startswith("$mathtrivia"):
        math_trivia = bot_req.get_math_trivia()
        await message.channel.send(
            html.unescape(
                f"{math_trivia[0]} True or false? The difficulty is {math_trivia[1]}.")
        )

        response = await bot.wait_for("message", check=check_message)

        if response.content.lower() == math_trivia[2].lower():
            await message.channel.send("You're correct!")
        else:
            await message.channel.send(
                f"Sorry, but the correct answer was {math_trivia[2]}.")

    if message.content.startswith("$animetrivia"):
        anime_trivia = bot_req.get_anime_trivia()
        await message.channel.send(
            html.unescape(
                f"{anime_trivia[0]} True or false? The difficulty is {anime_trivia[1]}."
            ))

        response = await bot.wait_for("message", check=check_message)

        if response.content.lower() == anime_trivia[2].lower():
            await message.channel.send("You're correct!")
        else:
            await message.channel.send(
                f"Sorry, but the correct answer was {anime_trivia[2]}.")


bot.run(os.getenv("XNONBOTTOKEN"))
