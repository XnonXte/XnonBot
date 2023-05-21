# Old XnonBot version that uses discord.py instead of discord.py.ext
# XnonBot Version Beta 0.1.1
import discord
import html
import random
import XnonBotModules.bot_req as bot_req
import os
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\dev.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

message_list = """
List of available commands (the prefix is '.'): 
    
`github` - Send the GitHub page for this bot
`hello` - Say "Hello!"
`about` - Send information about the bot, such as its purpose and features
`inspire` - Send a random inspirational quote to uplift the user
`contact` - Send contact information for the bot's creator
`roll` - Send a random dice roll result, from 1 to 6
`rps` - Play rock, paper, scissors with the user
`say` - Tell the bot to say something (the same message you're inputting with the commmand)
`help` - Send the list of available commands with their descriptions, so the user can easily explore and use them
`cat` - Send a random cat picture 
`dog` - Send a random dog picture
`waifu` - Send a random waifu picture (it's mostly SFW!)
`animaltrivia` - Send a random animal trivia and asking the user whether it's true or false
`mathtrivia` - Send a random math trivia and asking the user whether it's true or false
`animetrivia` - Send a random anime trivia and asking the user whether it's true or false
`pexels` - Search an image on pexels.com

Had an issue? Please pull an issue request on GitHub!
Have ideas for improving the bot? My DMs are open on XnonXte#2517
"""


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    msgcnt = message.content
    msgchn = message.channel

    def check_message(initial_requests):
        return (
            initial_requests.author == message.author
            and initial_requests.channel == msgchn
            and initial_requests.content.lower() in ["true", "false"]
        )

    if message.author == client.user:
        return

    if msgcnt.startswith(".help"):
        await msgchn.send(message_list)

    if msgcnt.startswith(".github"):
        await msgchn.send("https://github.com/XnonXte/XnonBot")

    if msgcnt.startswith(".hello"):
        await msgchn.send("Hello!")

    if msgcnt.startswith(".about"):
        await msgchn.send(
            "As the name implies, I'm a simple chatbot created by XnonXte!"
        )

    if msgcnt.startswith(".contact"):
        await msgchn.send("My DMs are always open at XnonXte#2517")

    if msgcnt.startswith(".roll"):
        await msgchn.send(random.randint(1, 6))

    if msgcnt.startswith(".dog"):
        dog_pic = bot_req.get_dog_pic()
        await msgchn.send(dog_pic)

    if msgcnt.startswith(".cat"):
        cat_pic = bot_req.get_cat_pic()
        await msgchn.send(cat_pic)

    if msgcnt.startswith(".inspire"):
        quote = bot_req.get_quote()
        await msgchn.send(quote)

    if msgcnt.startswith(".waifu"):
        waifu = bot_req.get_waifu_pic()
        await msgchn.send(waifu)

    if msgcnt.startswith(".animaltrivia"):
        animal_trivia = bot_req.get_animal_trivia()
        await msgchn.send(
            html.unescape(
                f"{animal_trivia[0]} True or false? The difficulty is {animal_trivia[1]}."
            )
        )

        response = await client.wait_for("message", check=check_message)

        if response.content.lower() == animal_trivia[2].lower():
            await msgchn.send("You're correct!")
        else:
            await msgchn.send(f"Sorry, but the correct answer was {animal_trivia[2]}.")

    if msgcnt.startswith(".mathtrivia"):
        math_trivia = bot_req.get_math_trivia()
        await msgchn.send(
            html.unescape(
                f"{math_trivia[0]} True or false? The difficulty is {math_trivia[1]}."
            )
        )

        response = await client.wait_for("message", check=check_message)

        if response.content.lower() == math_trivia[2].lower():
            await msgchn.send("You're correct!")
        else:
            await msgchn.send(f"Sorry, but the correct answer was {math_trivia[2]}.")

    if msgcnt.startswith(".animetrivia"):
        anime_trivia = bot_req.get_anime_trivia()
        await msgchn.send(
            html.unescape(
                f"{anime_trivia[0]} True or false? The difficulty is {anime_trivia[1]}."
            )
        )

        response = await client.wait_for("message", check=check_message)

        if response.content.lower() == anime_trivia[2].lower():
            await msgchn.send("You're correct!")
        else:
            await msgchn.send(f"Sorry, but the correct answer was {anime_trivia[2]}.")

    if msgcnt.startswith(".pexels"):
        try:
            if msgcnt == ".pexels" or not msgcnt.startswith(".pexels "):
                await msgchn.send("Please input a query after the command .pexels!")
                return
            query = msgcnt[8:]
            image_output = bot_req.get_pexels_photos(query)
            await msgchn.send(
                image_output[2]
                + " Photographer: "
                + image_output[0]
                + " - Powered by pexels.com"
            )
        except TypeError:
            await msgchn.send(
                "The image you're searching doesn't exist! Please try again with a different keyword"
            )

    if msgcnt.startswith(".rps"):
        if msgcnt == ".rps":
            await msgchn.send(
                "Please input either rock, paper, or scissors after the command .rps!"
            )
            return
        choices = ["rock", "paper", "scissors"]
        user_choice = msgcnt.split(" ")[1].lower()
        bot_choice = random.choice(choices)

        if user_choice not in choices:
            await msgchn.send(
                "Invalid choice. Please choose either rock, paper, or scissors."
            )
            return

        if user_choice == bot_choice:
            await msgchn.send(
                f"You chose {user_choice}. I chose {bot_choice}. We tied!"
            )
            return

        if user_choice == "rock" and bot_choice == "scissors":
            await msgchn.send(
                f"You chose {user_choice}. I chose {bot_choice}. You won!"
            )
        elif user_choice == "scissors" and bot_choice == "paper":
            await msgchn.send(
                f"You chose {user_choice}. I chose {bot_choice}. You won!"
            )
        elif user_choice == "paper" and bot_choice == "rock":
            await msgchn.send(
                f"You chose {user_choice}. I chose {bot_choice}. You won!"
            )
        else:
            await msgchn.send(f"You chose {user_choice}. I chose {bot_choice}. I won!")

    if msgcnt.startswith(".say "):
        say_output = msgcnt[5:]
        await msgchn.send(say_output)


client.run(os.getenv("XNONBOTTOKEN"))
