# XnonBot Version Beta 0.2.3
# Migrated to discord-py-interactions version 5x
# todo Buttons for trivia questions should be disabled after pressing, on which I haven't been done since migrating it to discord-py-interactions.
# todo All of the slash commands should be in different file, I should do OOP better lol.
# ? Add to ITB when?

import interactions
import random
import html

from interactions import (
    listen,
    slash_command,
    slash_option,
    SlashContext,
    slash_option,
    OptionType,
    ActionRow,
    ComponentContext,
    component_callback,
    message_context_menu,
    user_context_menu,
    ContextMenuContext,
    Message,
    Member,
    Button,
    ButtonStyle,
)
from XnonBotModules import bot_req
from os import getenv
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\dev.env")
bot = interactions.Client()

correct_trivia_answer = None

COMMANDS = """
List of avalaible commands (prompted using </> command):

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
`animaltrivia` - Send a random animal trivia and asking the user whether it's true or false
`mathtrivia` - Send a random math trivia and asking the user whether it's true or false
`animetrivia` - Send a random anime trivia and asking the user whether it's true or false

Have an issue with the bot? Please file a new issue on GitHub.
Want to contribute on the bot? Please send me a DM on discord (XnonXte#2517). 
"""

# Up-to-date as of 19/05/2023
waifu_category_list = (
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
)


@listen()
async def on_startup():
    print(f"The bot is running as {bot.user}!")
    print(
        """
 __   __                  ____        _   
 \ \ / /                 |  _ \      | |  
  \ V / _ __   ___  _ __ | |_) | ___ | |_ 
   > < | '_ \ / _ \| '_ \|  _ < / _ \| __|
  / . \| | | | (_) | | | | |_) | (_) | |_ 
 /_/ \_\_| |_|\___/|_| |_|____/ \___/ \__|
                                          
                                          
"""
    )
    print(
        "This bot is developed by XnonXte, refer to my GitHub for contact information. Enjoy using the bot!"
    )


@slash_command(name="hello", description="Say hello to the user.")
async def hello(ctx: SlashContext):
    await ctx.send(f"Hello there {ctx.user.mention}!")


@slash_command(name="help", description="Send a list of available slash commands.")
async def help(ctx: SlashContext):
    await ctx.send(COMMANDS)


@slash_command(name="say", description="Tell the bot to say something.")
@slash_option(
    opt_type=OptionType.STRING,
    name="message",
    description="Message to send",
    required=True,
)
async def say(ctx: SlashContext, message: str):
    await ctx.send(f"{ctx.user.mention} said: `{message}`")


@slash_command(name="about", description="Send the information about this bot.")
async def about(ctx: SlashContext):
    await ctx.send("As the name implies, I'm a simple chatbot created by XnonXte!")


@slash_command(name="roll", description="Choose a random dice roll (1 to 6).")
async def roll(ctx: SlashContext):
    await ctx.send(random.randint(1, 6))


@slash_command(name="github", description="Send the github page for this bot.")
async def github(ctx: SlashContext):
    await ctx.send("https://github.com/XnonXte/XnonBot")


@slash_command(name="quote", description="Get a random quote from zenquotes.io")
async def quote(ctx: SlashContext):
    quote = bot_req.get_quote()
    await ctx.send(quote)


@slash_command(
    name="waifu",
    description="Get a random waifu picture from https://waifu.pics/docs (it's SFW don't worry!)",
)
@slash_option(
    opt_type=OptionType.STRING,
    name="category",
    description="Enter the category (e.g. 'waifu', refer to https://waifu.pics/docs for more information!)",
    required=True,
)
async def waifu(ctx: SlashContext, category: str):
    if category not in waifu_category_list:
        await ctx.send("Please enter a valid category!", ephemeral=True)
        return
    else:
        waifu_pic = bot_req.get_waifu_pic(category)
        await ctx.send(waifu_pic)


@slash_command(
    name="dog", description="Get a random dog picture from https://dog.ceo/dog-api"
)
async def dog(ctx: SlashContext):
    dog = bot_req.get_dog_pic()
    await ctx.send(dog)


@slash_command(
    name="cat", description="Get a random cat picture from https://thecatapi.com"
)
async def cat(ctx: SlashContext):
    cat = bot_req.get_cat_pic()
    await ctx.send(cat)


@slash_command(name="rps", description="Play rock, paper, scissors with the user.")
@slash_option(
    opt_type=OptionType.STRING,
    name="choice",
    description="Enter your choice (rock, paper, scissors).",
    required=True,
)
async def rps(ctx: SlashContext, choice: str):
    choices = ("rock", "paper", "scissors")
    bot_choice = random.choice(choices)

    if choice not in choices:
        await ctx.send(
            "Invalid choice. Please choose either rock, paper, or scissors!",
            ephemeral=True,
        )
        return

    if choice == bot_choice:
        await ctx.send(
            f"{ctx.user.mention} chose {choice}. I chose {bot_choice}. We tied!"
        )
    elif choice == "rock" and bot_choice == "scissors":
        await ctx.send(
            f"{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!"
        )
    elif choice == "scissors" and bot_choice == "paper":
        await ctx.send(
            f"{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!"
        )
    elif choice == "paper" and bot_choice == "rock":
        await ctx.send(
            f"{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} chose {choice}. I chose {bot_choice}. I won!"
        )


@slash_command(name="pexels", description="Search an image on pexels.com")
@slash_option(
    opt_type=OptionType.STRING,
    name="search_query",
    description="Image to search",
    required=True,
)
async def pexels(ctx: SlashContext, search_query: str):
    image_output = bot_req.get_pexels_photos(search_query)
    await ctx.send(
        f"An image of {search_query} has been generated! Photographed by: {image_output[0]}, original link: {image_output[2]} - Powered by pexels.com"
    )


@slash_command(name="animaltrivia", description="Play a random animal trivia game.")
async def animaltrivia(ctx: SlashContext):
    global correct_trivia_answer
    animal_trivia = bot_req.get_animal_trivia()
    await ctx.send(
        html.unescape(f"{animal_trivia[0]} | The difficulty is {animal_trivia[1]}.")
    )

    components: list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.PRIMARY,
                custom_id="animal_trivia_button_true",
                label="True",
            ),
            Button(
                style=ButtonStyle.DANGER,
                custom_id="animal_trivia_button_false",
                label="False",
            ),
        )
    ]

    await ctx.send(
        f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.",
        components=components,
        ephemeral=True,
    )
    correct_trivia_answer = animal_trivia[2]


@component_callback("animal_trivia_button_true")
async def animal_trivia_button_true(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "true":
        await ctx.send(
            f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}."
        )


@component_callback("animal_trivia_button_false")
async def animal_trivia_button_false(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "false":
        await ctx.send(
            f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}."
        )


@slash_command(
    name="mathtrivia",
    description="Play a random math trivia game.",
)
async def mathtrivia(ctx: SlashContext):
    global correct_trivia_answer
    math_trivia = bot_req.get_math_trivia()
    await ctx.send(
        html.unescape(f"{math_trivia[0]} | The difficulty is {math_trivia[1]}.")
    )

    components = list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.PRIMARY,
                custom_id="math_trivia_button_true",
                label="True",
            ),
            Button(
                style=ButtonStyle.DANGER,
                custom_id="math_trivia_button_false",
                label="False",
            ),
        )
    ]
    await ctx.send(
        f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.",
        components=components,
        ephemeral=True,
    )
    correct_trivia_answer = math_trivia[2]


@component_callback("math_trivia_button_true")
async def math_trivia_button_true(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "true":
        await ctx.send(
            f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}"
        )


@component_callback("math_trivia_button_false")
async def math_trivia_button_false(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "false":
        await ctx.send(
            f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}"
        )


@slash_command(
    name="animetrivia",
    description="Play a random animal trivia game.",
)
async def animetrivia(ctx: SlashContext):
    global correct_trivia_answer
    anime_trivia = bot_req.get_anime_trivia()
    await ctx.send(
        html.unescape(f"{anime_trivia[0]} | The difficulty is {anime_trivia[1]}.")
    )

    components = list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.PRIMARY,
                custom_id="anime_trivia_button_true",
                label="True",
            ),
            Button(
                style=ButtonStyle.DANGER,
                custom_id="anime_trivia_button_false",
                label="False",
            ),
        )
    ]
    await ctx.send(
        f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.",
        components=components,
        ephemeral=True,
    )
    correct_trivia_answer = anime_trivia[2]


@component_callback("anime_trivia_button_true")
async def anime_trivia_button_true(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "true":
        await ctx.send(
            f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}"
        )


@component_callback("anime_trivia_button_false")
async def anime_trivia_button_false(ctx: ComponentContext):
    if correct_trivia_answer.lower() == "false":
        await ctx.send(
            f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!"
        )
    else:
        await ctx.send(
            f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}"
        )


# This opens up if you right-click a message and choose Apps.
@message_context_menu(name="Repeat")
async def repeat(ctx: ContextMenuContext):
    message: Message = ctx.target
    await ctx.send(message.content)


@message_context_menu(name="Help")
async def ping(ctx: ContextMenuContext):
    await ctx.send(COMMANDS)


@message_context_menu(name="Quickstart (message)")
async def quickstart_message(ctx: ContextMenuContext):
    await ctx.send(
        f"Hello there {ctx.user.mention}! Thank you for using XnonBot on discord. You can either use `/help` or `$help` to prompt all the available commands for this bot.",
        ephemeral=True,
    )


# This opens up if you right-click a user and choose Apps.
@user_context_menu(name="Ping")
async def ping(ctx: ContextMenuContext):
    member: Member = ctx.target
    await ctx.send(f"Pong {member.mention}!")


@user_context_menu(name="Quickstart (user)")
async def quickstart_usere(ctx: ContextMenuContext):
    await ctx.send(
        f"Hello there {ctx.user.mention}! Thank you for using XnonBot on discord. You can either use `/help` or `$help` to prompt all the available commands for this bot.",
        ephemeral=True,
    )


bot.start(getenv("XNONBOTTOKEN"))
