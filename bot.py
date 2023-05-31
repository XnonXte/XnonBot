import discord
import random
import os
import html
import wikipedia
import textwrap
from dotenv import load_dotenv
from XnonBotModules import bot_requests, components, keep_alive

load_dotenv("C:\Programming\XnonBot\.env")

version = "Beta 0.4.3.2"
prefix = ";"
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix=prefix, intents=intents)

# Command groups.
xb = discord.SlashCommandGroup("xnonbot", "general commands")
cfg = discord.SlashCommandGroup("config", "moderator only commands")

# Subgroups of the group xb.
gen = xb.create_subgroup("generate", "generate related command")
game = xb.create_subgroup("game", "games related commmands")
util = xb.create_subgroup("utility", "utilities related commands")
wk = xb.create_subgroup("wikipedia", "wikipedia related commands")

SLASHCOMMANDS = """
`quickstart` - Sends a quickstart message
`help` - Prompts help message
`about` - Sends information regarding this bot
`quote` - Sends a random inspirational quote
`roll` - Sends a random dice roll result, from 1 to 6
`rps` - Plays rock, paper, scissors with the user
`cat` - Sends a random cat picture
`dog` - Sends a random dog picture
`waifu` - Sends a random waifu picture (it's SFW!)
`pexels` - Search for an image on pexels.com
`trivia` - Sends a random  trivia question and asking the user whether it's true or false
`convertticks` - Converts ticks to seconds
`convertseconds` - Converts seconds to ticks
`ping` - Checks the bot's latency
`gtn` - Plays a guess-the-number game
`dadjoke` - Gets a random dad joke
`wyr` - Gets a random would-you-rather question
`summary` - Gets summary of a Wikipedia article
`link` - Gets a Wikipedia link
"""


@bot.event
async def on_ready():
    print(
        """
db    db d8b   db  .d88b.  d8b   db d8888b.  .d88b.  d888888b 
`8b  d8' 888o  88 .8P  Y8. 888o  88 88  `8D .8P  Y8. `~~88~~' 
 `8bd8'  88V8o 88 88    88 88V8o 88 88oooY' 88    88    88    
 .dPYb.  88 V8o88 88    88 88 V8o88 88~~~b. 88    88    88    
.8P  Y8. 88  V888 `8b  d8' 88  V888 88   8D `8b  d8'    88    
YP    YP VP   V8P  `Y88P'  VP   V8P Y8888P'  `Y88P'     YP    
                                                              
                                                              
"""
    )
    print(
        f"We have logged in as {bot.user}. | Visit my GitHub: https://github.com/XnonXte"
    )


# Events that read message contents.
@bot.event
async def on_member_join(ctx, member):
    await ctx.respond(f"Please welcome {member.mention} to the server!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith(f"{prefix}quickstart"):
        await message.channel.send(
            "Thank you for using XnonBot! You can start by prompting `/help` to get started."
        )


"""XnonBot command group"""


@xb.command(name="quickstart", description="Sends a quickstart message.")
async def quickstart(ctx):
    await ctx.respond(
        "Thank you for using XnonBot! You can start by prompting `/help` to get started."
    )


@xb.command(description="Says hello to the user.")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.user.mention}!")


@xb.command(description="Overview of available slash commands.")
async def help(ctx):
    help_message_embed = discord.Embed(
        description="Thank you for using XnonBot! Created with 💖 by XnonXte.",
        color=discord.Colour.from_rgb(0, 217, 255),
    )
    help_message_embed.add_field(name="Commands", value=SLASHCOMMANDS)

    help_message_embed.set_author(
        name="Help & About",
        icon_url="attachment://xnonbot.png",
    )
    help_message_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="attachment://xnonbot.png",
    )
    help_message_embed.set_thumbnail(url="attachment://xnonbot.png")

    await ctx.respond(
        file=discord.File("local\\xnonbot.png", filename="xnonbot.png"),
        embed=help_message_embed,
        view=components.HelpButtons(),
    )


@xb.command(description="Official GitHub page for this bot.")
async def github(ctx):
    await ctx.respond("https://github.com/XnonXte/XnonBot")


"""Utility subgroup"""


@util.command(description="Checks the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! My ping is {round(bot.latency * 100, 2)}ms.")


@util.command(description="Converts ticks to seconds.")
async def convertticks(
    ctx, value: discord.Option(str, description="Enter the value in ticks.")
):
    convert = value * 0.015
    await ctx.respond(f"{value} ticks is equal to {convert} seconds.")


@util.command(description="Converts seconds to ticks.")
async def convertseconds(
    ctx, value: discord.Option(float, description="Enter the value in seconds.")
):
    convert = value / 0.015
    await ctx.respond(f"{value} seconds is equal to {int(convert)} ticks.")


"""Generate subgroup"""


@gen.command(description="Gets a random quote from zenquotes.io")
async def quote(ctx):
    quote = bot_requests.get_quote()
    await ctx.respond(quote)


@gen.command(
    description="Gets a random waifu picture from https://waifu.pics/docs (It's SFW!)"
)
async def waifu(
    ctx,
    category: discord.Option(
        str,
        description="Select the category (Example 'waifu', please refer to https://waifu.pics/docs for more categories!)",
    ),
):
    waifu_pic = bot_requests.get_waifu_pic(category)
    if waifu_pic is None:  # If the category that the user requesting doesn't exist
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return

    waifu_embed = discord.Embed(
        title="Waifu generated!",
        description=f"Here's a(n) {category} image for you.",
    )
    waifu_embed.set_image(url=waifu_pic)

    await ctx.respond(embed=waifu_embed)


@gen.command(description="Gets a random dog picture from https://dog.ceo/dog-api")
async def dog(ctx):
    dog = bot_requests.get_dog_pic()
    dog_embed = discord.Embed(
        title="Bark!",
        description="Random dog picture generated.",
    )
    dog_embed.set_image(url=dog)

    await ctx.respond(embed=dog_embed)


@gen.command(description="Gets a random cat picture from https://thecatapi.com")
async def cat(ctx):
    cat = bot_requests.get_cat_pic()
    cat_embed = discord.Embed(
        title="Meow!",
        description="Random cat picture generated.",
    )
    cat_embed.set_image(url=cat)

    await ctx.respond(embed=cat_embed)


@gen.command(description="Search for an image on pexels.com")
async def pexels(
    ctx, search_query: discord.Option(str, description="Image to search.")
):
    try:
        image_output = bot_requests.get_pexels_photos(search_query)

        pexels_output_embed = discord.Embed(
            title="Image from pexels generated!",
            description=f"Here's a(n) {search_query} image for you.",
        )
        pexels_output_embed.set_image(url=image_output)

        await ctx.respond(embed=pexels_output_embed)
    except Exception as e:
        await ctx.respond(f"An error has been encountered: {e}", ephemeral=True)


@gen.command(description="Generates a random would you rather question.")
async def wyr(ctx):
    would_you_rather = bot_requests.get_would_you_rather()
    await ctx.respond(would_you_rather)


@gen.command(description="Generates a random dad joke.")
async def dadjoke(ctx):
    dad_joke = bot_requests.get_dad_joke()
    await ctx.respond(dad_joke)


"""Game subgroup"""


@game.command(description="Chooses a random dice roll (1 to 6).")
async def roll(ctx):
    await ctx.respond(random.randint(1, 6))


@game.command(description="Plays a trivia game from https://opentdb.com")
async def trivia(
    ctx,
    category: discord.Option(
        str,
        description="Choose the category (Example 'animal', refer to the GitHub page for more categories).",
    ),
):
    trivia_question = bot_requests.get_trivia(category.lower())
    if (
        trivia_question is None
    ):  # If the category that the user requesting doesn't exist
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return
    correct_trivia_answer = trivia_question[2]

    await ctx.respond(
        html.unescape(f"The difficulty is {trivia_question[1]} - {trivia_question[0]}")
    )

    await ctx.respond(
        f"Please select your answer!",
        view=components.TriviaButtons(ctx.author, correct_trivia_answer),
    )


@game.command(description="Guess the number game.")
async def gtn(ctx, max: discord.Option(int, description="Maximum number to guess.")):
    random_number = random.randint(0, max)

    await ctx.respond(f"Guess the number (maximum: {max})")
    response = await bot.wait_for(
        "message", check=lambda message: message.author == ctx.author
    )  # Tell the bot to wait for a message, it must be sent by the same user.

    if int(response.content) == random_number:
        await ctx.send(f"You've guessed it right! The number is {random_number}.")
    elif int(response.content) > max:
        await ctx.send(f"That's too high! The max number is {max}.")
    else:
        return  # If the message wasn't an integer.


@game.command(description="Plays rock, paper, scissors with the user.")
async def rps(
    ctx,
    choice: discord.Option(str, description="Choose either rock, paper, or scissors."),
):
    rps_choices = ("rock", "paper", "scissors")
    bot_choice = random.choice(rps_choices)
    user_choice = choice.lower()

    if user_choice not in rps_choices:
        await ctx.respond(
            "Invalid choice. Please choose either rock, paper, or scissors!",
            ephemeral=True,
        )
        return
    elif user_choice == bot_choice:
        output = "We tied!"
    elif user_choice == "rock" and bot_choice == "scissors":
        output = "You won!"
    elif user_choice == "paper" and bot_choice == "rock":
        output = "You won!"
    elif user_choice == "scissors" and bot_choice == "paper":
        output = "You won!"
    else:
        output = "You lost!"

    rps_embed = discord.Embed(
        title="Rock, paper, scissors", color=discord.Color.from_rgb(0, 217, 255)
    )
    rps_embed.add_field(
        name="Results:",
        value=f"You choose ***{choice}***\n Computer chooses ***{bot_choice}***\n\n {output}",
    )

    await ctx.respond(embed=rps_embed)


"""Wikipedia subgroup"""


@wk.command(description="Searches for a summary in Wikipedia.")
async def summary(
    ctx,
    search: discord.Option(str, description="What to look for and create a summary."),
):
    await ctx.channel.trigger_typing()

    try:
        wikipedia_page = wikipedia.page(search)
        wikipedia_summary = wikipedia_page.summary
        wikipedia_url = wikipedia_page.url

        chars_limit = 950
        if (
            len(wikipedia_summary) > chars_limit
        ):  # We want it to be less than 1054 characters.
            wikipedia_summary = textwrap.shorten(wikipedia_summary, width=chars_limit)

        wikipedia_summary_embed = discord.Embed(
            title=f"Wikipedia summary of {search}",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        wikipedia_summary_embed.add_field(name="Summary", value=wikipedia_summary)
        wikipedia_summary_embed.add_field(
            name="Original link", value=wikipedia_url, inline=False
        )
        wikipedia_summary_embed.set_thumbnail(url="attachment://wikipedia.png")

        try:
            await ctx.respond(
                file=discord.File("local\\wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_summary_embed,
            )  # If the bot can't send an interaction response for whatever reason.
        except:
            await ctx.send(
                file=discord.File(
                    "local\\wikipedia.png",
                    filename="wikipedia.png",
                ),
                embed=wikipedia_summary_embed,
            )
    except wikipedia.DisambiguationError as e:
        exception_embed = discord.Embed(
            title="DisambiguationError, please specify your search query with the options below",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        exception_embed.add_field(name=f"{search} may refer to:", value=e.options)

        await ctx.respond(
            f"Oops, an error occured!", embed=exception_embed, ephemeral=True
        )
    except Exception as e:
        await ctx.respond(e, ephemeral=True)


@wk.command(description="Searches for a link in Wikipedia")
async def link(ctx, query: discord.Option(str, description="The link to search for.")):
    await ctx.channel.trigger_typing()

    try:
        link_summary = wikipedia.summary(query, auto_suggest=False)
        search = query.lower().replace(" ", "_").replace("  ", "_")

        wikipedia_link_embed = discord.Embed(
            title="I've got one!",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        wikipedia_link_embed.add_field(
            name=f"Wikipedia link for {query}",
            value=f"https://en.wikipedia.org/wiki/{search}",
        )
        wikipedia_link_embed.set_thumbnail(url="attachment://wikipedia.png")

        try:
            await ctx.respond(
                file=discord.File("local\\wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_link_embed,
            )
        except:
            await ctx.send(
                file=discord.File("local\\wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_link_embed,
            )
    except wikipedia.DisambiguationError as e:
        exception_embed = discord.Embed(
            title="DisambiguationError, please specify your search query with the options below",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        exception_embed.add_field(name=f"{query} may refer to:", value=e.options)

        await ctx.respond(
            f"Oops, an error occured!", embed=exception_embed, ephemeral=True
        )
    except Exception as e:
        await ctx.respond(e, ephemeral=True)


"""Context menus"""


@bot.message_command(name="Repeat")
async def repeat(ctx, message: discord.Message):
    await ctx.respond(message.content)


@bot.user_command(name="Creation date")
async def creation_date(ctx, member: discord.Member):
    await ctx.respond(
        f"The account {member.name} was created at `{member.created_at}`."
    )


@bot.user_command(name="Join date")
async def join_date(ctx, member: discord.Member):
    await ctx.respond(f"The account {member.name} joined at `{member.joined_at}`.")


@bot.user_command(name="Ping")
async def ping_ctx_menu(ctx, member: discord.Member):
    await ctx.respond(f"Hi {member.mention}.")


# Add the groups that we have created earlier to discord.
bot.add_application_command(xb)
bot.add_application_command(cfg)

# Keep running the bot.
keep_alive.keep_alive()

# Actually running the bot.
bot.run(os.getenv("XNONBOTTOKEN"))
