# XnonBot Version Beta 0.3
# Migrated to discord-py-interactions version 5x
# * Fixed the issue with pressing buttons.
# * Added a lot more comments.
# todo All of the slash commands should be in different file with classes and stuff, I should do OOP better lol.
# ? Add to ITB when?

import interactions
import random
import html
from interactions import (
    listen,
    slash_command,
    slash_option,
    SlashContext,
    OptionType,
    message_context_menu,
    user_context_menu,
    ContextMenuContext,
    Message,
    Member,
    Button,
    ButtonStyle,
)
from XnonBotModules import bot_req, keep_alive
from interactions.api.events import Component
import os

bot = interactions.Client()

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
`trivia` - Send a random  trivia question and asking the user whether it's true or false
`convertticks` - Convert ticks to seconds.
`convertseconds` - Convert seconds to ticks.

There's also a couple of context menus that you'd have to look up by yourself. Have fun using the bot!
"""

# Also available on the Github page.
trivia_category_list = [
    "animal",
    "anime",
    "math",
    "history",
    "geography",
    "art",
    "celebrity",
    "computers",
    "sports",
    "cartoons",
]

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
async def on_startup():  # We're using on_startup() instead of on_ready() because of interactions.py version 5, but both are mostly the same.
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


# Every functions starting with the @slash_command decorator will be able to be prompted with </> command on discord.
@slash_command(name="hello", description="Say hello to the user.")
async def hello(ctx: SlashContext):
    await ctx.send(f"Hello there {ctx.user.mention}!")


@slash_command(name="help", description="Send a list of available slash commands.")
async def help(ctx: SlashContext):
    await ctx.send(COMMANDS)


# In this instance, we're using @slash_option to make an option for our slash command, we'll be using much of this later on.
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
    if (
        category not in waifu_category_list
    ):  # If the category that the user is inputting doesn't exist, we're using ephemeral=True so it's only viewable by the user.
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


@slash_command(
    name="trivia",
    description="Play a trivia game (database from https://opentdb.com/).",
    scopes=[1103578001318346812],
)
@slash_option(
    opt_type=OptionType.STRING,
    name="category",
    description="Choose a category (e.g. 'animal', refer to github for the list of available trivia categories.)).",
    required=True,
)
async def trivia(ctx: SlashContext, category: str):
    if category not in trivia_category_list:
        await ctx.send(
            "Invalid category, please try again! (Please refer to the GitHub page for the available categories).",
            ephemeral=True,
        )
        return

    global trivia_button_true, trivia_button_false, trivia_message, correct_trivia_answer  # We're using the global keyword to store the necesarry variables globally since it's necesarry to have them in later decorator.
    trivia_question = bot_req.get_trivia(category)
    correct_trivia_answer = trivia_question[2]

    await ctx.send(
        html.unescape(f"{trivia_question[0]} | The difficulty is {trivia_question[1]}")
    )

    trivia_button_true = Button(
        style=ButtonStyle.PRIMARY,
        label="True",
        custom_id="button_true",
        disabled=False,
    )
    trivia_button_false = Button(
        style=ButtonStyle.DANGER,
        label="False",
        custom_id="button_false",
        disabled=False,
    )

    trivia_message = await ctx.send(
        f"Please choose your answer {ctx.user.mention}.",
        components=[trivia_button_true, trivia_button_false],
    )


@listen()
async def on_component(event: Component):
    ctx = event.ctx

    if (
        ctx.client != event.client
    ):  # Check if the user pressing the button is the same person as the one requesting them; otherwise, return ().
        return

    trivia_button_true.disabled = trivia_button_false.disabled = True
    await trivia_message.edit(components=[trivia_button_true, trivia_button_false])

    if ctx.custom_id == "button_true":
        if correct_trivia_answer.lower() == "true":
            await ctx.send(
                f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!"
            )
        else:
            await ctx.send(
                f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}."
            )

    elif ctx.custom_id == "button_false":
        if correct_trivia_answer.lower() == "false":
            await ctx.send(
                f"{ctx.user.mention} chooses False, {ctx.user.mention} is correct!"
            )
        else:
            await ctx.send(
                f"{ctx.user.mention} chooses False. Sorry, but the correct answer was {correct_trivia_answer}."
            )


@slash_command(name="convertticks", description="Convert ticks to seconds.")
@slash_option(
    opt_type=OptionType.INTEGER,
    name="value",
    description="Enter the value.",
    required=True,
)
async def convertticks(ctx: SlashContext, value: int):
    convert = (
        value * 0.015
    )  # Converting ticks to seconds; 1 tick is equal to 0.015 seconds.
    await ctx.send(f"{value} ticks is equal to {convert} seconds.")


@slash_command(name="convertseconds", description="Convert seconds to ticks.")
@slash_option(
    opt_type=OptionType.NUMBER,
    name="value",
    description="Enter the value in seconds.",
    required=True,
)
async def convertseconds(ctx: SlashContext, value: float):
    convert = value / 0.015
    await ctx.send(f"{value} seconds is equal to {int(convert)} ticks.")


# This opens up if you right-click a message and choose Apps.
@message_context_menu(name="Repeat")
async def repeat(ctx: ContextMenuContext):
    message: Message = ctx.target
    await ctx.send(message.content)


@message_context_menu(name="Help")
async def helpcmctx(ctx: ContextMenuContext):
    await ctx.send(COMMANDS)


@message_context_menu(name="Quickstart")
async def quickstart_message(ctx: ContextMenuContext):
    await ctx.send(
        f"Hello there {ctx.user.mention}! Thank you for using XnonBot on discord. You can use `/help` to prompt all the available commands for this bot.",
        ephemeral=True,
    )


# This opens up if you right-click a user and choose Apps.
@user_context_menu(name="Ping")
async def ping(ctx: ContextMenuContext):
    member: Member = ctx.target
    await ctx.send(f"Pong {member.mention}!")


# Actually running the bot, change the token with yours if you want to run this bot for yourself.
keep_alive.keep_alive()
bot.start(os.environ["XNONBOTTOKEN"])
