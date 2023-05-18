# XnonBot Version Beta 0.2.1
# Currently written for interactions.py version 4 but it might be migrated to version 5 in the near future.
import interactions
import BotRequests
import html
import random

from interactions import Option, OptionType, CommandContext, ComponentContext, Button, ButtonStyle, ActionRow
from dotenv import load_dotenv
from os import getenv

load_dotenv("C:\Programming\XnonBot\dev.env")
token = getenv("XNONBOTTOKEN") # Token for XnonBot#8699 on discord
bot = interactions.Client(token=token)

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
`waifu` - Send a random waifu picture (it's mostly SFW!)
`pexels` - Search an image on pexels.com
`animaltrivia` - Send a random animal trivia and asking the user whether it's true or false
`mathtrivia` - Send a random math trivia and asking the user whether it's true or false
`animetrivia` - Send a random anime trivia and asking the user whether it's true or false
"""


@bot.event
async def on_ready():
    print("The bot is now running!")


@bot.command(name="hello", description="Say hello to the user.")
async def hello(ctx: CommandContext):
    await ctx.send(f"Hello there {ctx.user.mention}!")


@bot.command(name="help", description="Send a list of available slash commands.")
async def help(ctx: CommandContext):
    await ctx.send(COMMANDS)


@bot.command(
    name="say",
    description="Tell the bot to say something.",
    options=[
        Option(
            type=OptionType.STRING,
            name="message",
            description="Message to send",
            required=True,
        ),
    ],
)
async def say(ctx: CommandContext, message: str):
    await ctx.send(f"{ctx.user.mention} said: `{message}`")


@bot.command(name="about", description="Send the information about this bot.")
async def about(ctx: CommandContext):
    await ctx.send("As the name implies, I'm a simple chatbot created by XnonXte!")


@bot.command(name="roll", description="Choose a random dice roll (1 to 6).")
async def roll(ctx: CommandContext):
    await ctx.send(random.randint(1, 6))


@bot.command(name="github", description="Send the github page for this bot.")
async def github(ctx: CommandContext):
    await ctx.send("https://github.com/XnonXte/XnonBot")


@bot.command(name="quote", description="Get a random quote.")
async def quote(ctx: CommandContext):
    quote = BotRequests.get_quote()
    await ctx.send(quote)


@bot.command(name="waifu", description="Get a random waifu picture.")
async def waifu(ctx: CommandContext):
    waifu = BotRequests.get_waifu_pic()
    await ctx.send(waifu)


@bot.command(name="dog", description="Get a random dog picture.")
async def dog(ctx: CommandContext):
    dog = BotRequests.get_dog_pic()
    await ctx.send(dog)


@bot.command(name="cat", description="Get a random cat picture.")
async def cat(ctx: CommandContext):
    cat = BotRequests.get_cat_pic()
    await ctx.send(cat)


@bot.command(
    name="rps",
    description="Play rock, paper, scissors with the user.",
    options=[
        Option(
            type=OptionType.STRING,
            name="choice",
            description="Input your choice (rock, paper, or scissors)",
            required=True,
        ),
    ],
)
async def rps(ctx: CommandContext, choice: str):
    choices = ("rock", "paper", "scissors")
    bot_choice = random.choice(choices)

    if choice not in choices:
        await ctx.send(
            'Invalid choice. Please choose either rock, paper, or scissors!', ephemeral=True)
        return

    if choice == bot_choice:
        await ctx.send(
            f'{ctx.user.mention} chose {choice}. I chose {bot_choice}. We tied!')
    elif choice == 'rock' and bot_choice == 'scissors':
        await ctx.send(
            f'{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!')
    elif choice == 'scissors' and bot_choice == 'paper':
        await ctx.send(
            f'{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!')
    elif choice == 'paper' and bot_choice == 'rock':
        await ctx.send(
            f'{ctx.user.mention} chose {choice}. I chose {bot_choice}. {ctx.user.mention} won!')
    else:
        await ctx.send(
            f'{ctx.user.mention} chose {choice}. I chose {bot_choice}. I won!')


@bot.command(
    name="pexels",
    description="Search an image on pexels.com",
    options=[
        Option(
            type=OptionType.STRING,
            name="search_query",
            description="Image to search",
            required=True
        )
    ]
)
async def pexels(ctx: CommandContext, search_query: str):
    image_output = BotRequests.get_pexels_photos(search_query)
    await ctx.send(f"An image of {search_query} has been generated! Photographed by: {image_output[0]}, original link: {image_output[2]} - Powered by pexels.com")


@bot.command(
    name="animaltrivia",
    description="Play a random animal trivia game.", 
)
async def animaltrivia(ctx: CommandContext):
    global correct_trivia_answer
    animal_trivia = BotRequests.get_animal_trivia()
    await ctx.send(html.unescape(f"{animal_trivia[0]} | The difficulty is {animal_trivia[1]}."))
    
    button = Button(
        style=ButtonStyle.PRIMARY,
        custom_id="animal_trivia_button_true",
        label="True",
    )
    button2 = Button(
        style=ButtonStyle.DANGER,
        custom_id="animal_trivia_button_false",
        label="False",
    )
    action_row = ActionRow(components=[button, button2])
    await ctx.send(f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.", components=action_row)
    correct_trivia_answer = animal_trivia[2] 


@bot.component("animal_trivia_button_true")
async def animal_trivia_button_true(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "true":
        await ctx.send(f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}.")


@bot.component("animal_trivia_button_false")
async def animal_trivia_button_false(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "false":
        await ctx.send(f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}.")


@bot.command(
    name="mathtrivia",
    description="Play a random math trivia game.", 
)
async def mathtrivia(ctx: CommandContext):
    global correct_trivia_answer
    math_trivia = BotRequests.get_math_trivia()
    await ctx.send(html.unescape(f"{math_trivia[0]} | The difficulty is {math_trivia[1]}."))
    
    button = Button(
        style=ButtonStyle.PRIMARY,
        custom_id="math_trivia_button_true",
        label="True",
    )
    button2 = Button(
        style=ButtonStyle.DANGER,
        custom_id="math_trivia_button_false",
        label="False",
    )
    action_row = ActionRow(components=[button, button2])
    await ctx.send(f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.", components=action_row, ephemeral=True)
    correct_trivia_answer = math_trivia[2] 


@bot.component("math_trivia_button_true")
async def math_trivia_button_true(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "true":
        await ctx.send(f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}")


@bot.component("math_trivia_button_false")
async def math_trivia_button_false(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "false":
        await ctx.send(f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}")


@bot.command(
    name="animetrivia",
    description="Play a random animal trivia game.", 
)
async def animetrivia(ctx: CommandContext):
    global correct_trivia_answer
    anime_trivia = BotRequests.get_anime_trivia()
    await ctx.send(html.unescape(f"{anime_trivia[0]} | The difficulty is {anime_trivia[1]}."))
    
    
    button = Button(
        style=ButtonStyle.PRIMARY,
        custom_id="anime_trivia_button_true",
        label="True",
    )
    button2 = Button(
        style=ButtonStyle.DANGER,
        custom_id="anime_trivia_button_false",
        label="False",
    )
    action_row = ActionRow(components=[button, button2])
    await ctx.send(f"Please choose an answer {ctx.user.mention}, on whether you think that is true or false.", components=action_row, ephemeral=True)
    correct_trivia_answer = anime_trivia[2] 


@bot.component("anime_trivia_button_true")
async def anime_trivia_button_true(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "true":
        await ctx.send(f"{ctx.user.mention} choose True, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose True. Sorry, but the correct answer was {correct_trivia_answer}")


@bot.component("anime_trivia_button_false")
async def anime_trivia_button_false(ctx: ComponentContext):  
    if correct_trivia_answer.lower() == "false":
        await ctx.send(f"{ctx.user.mention} choose False, {ctx.user.mention} is correct!")
    else:
        await ctx.send(f"{ctx.user.mention} choose False. Sorry, but the correct answer was {correct_trivia_answer}")

    
bot.start()
