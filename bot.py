import discord
import random
import os
import html
import wikipedia
import textwrap
import asyncio
from dotenv import load_dotenv
from BotModules import keep_alive, xnonbot_components, xnonbot_requests

load_dotenv("C:\Programming\XnonBot\dev.env")

version = "v0.4.4.1"

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

# Command groups.
gen = discord.SlashCommandGroup("generate", "generate related command")
game = discord.SlashCommandGroup("game", "games related commmands")
util = discord.SlashCommandGroup("utility", "utilities related commands")
wk = discord.SlashCommandGroup("wikipedia", "wikipedia related commands")

SLASHCOMMANDS = """
`quickstart` - Sends a quickstart message
`help` - Prompts help message
`about` - Sends information regarding this bot
`quote` - Sends a random inspirational quote
`roll` - Sends a random dice roll result, from 1 to 6
`rps` - Plays rock, paper, scissors with the user
`cat` - Sends a random cat picture
`dog` - Sends a random dog picture
`waifu` - Sends a random waifu picture
`pexels` - Search for an image on pexels.com
`trivia` - Sends a random  trivia question and asking the user whether it is True or False
`conversion_ticks` - Converts ticks to seconds and vice versa
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
        f"The bot is now running as {bot.user} - Visit my GitHub: https://github.com/XnonXte"
    )


@bot.event
async def on_member_join(ctx, member):
    await ctx.respond(f"Please welcome {member.mention} to the server!")


@bot.command(description="Sends a quickstart message.")
async def quickstart(ctx):
    await ctx.respond(
        "Thank you for using XnonBot! You can start by prompting `/help` to get started."
    )


@bot.command(description="Says hello to the user.")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.user.mention}!")


@bot.command(description="Overview of available slash commands.")
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
        file=discord.File("local/xnonbot.png", filename="xnonbot.png"),
        embed=help_message_embed,
        view=xnonbot_components.HelpButtons(),
    )


@bot.command(description="Official GitHub page for this bot.")
async def github(ctx):
    await ctx.respond("https://github.com/XnonXte/XnonBot")


"""Utility command group"""


@util.command(description="Checks the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! My ping is {round(bot.latency * 100, 2)}ms.")


@util.command(description="Converts tick to second and vice versa.")
async def conversion_ticks(
    ctx,
    value: discord.Option(float, description="Enter the value."),
    value_type: discord.Option(
        choices=["ticks", "seconds"],
        description="Select which value_type are you inputting.",
    ),
):
    if value_type == "ticks":
        calculate = value * 0.015
        await ctx.respond(f"{value} ticks equals to {calculate} seconds.")
    elif value_type == "seconds":
        calculate = value / 0.015
        await ctx.respond(f"{value} seconds equals to {calculate} ticks.")


"""Generate command group"""


@gen.command(description="Gets a random quote from zenquotes.io")
async def quote(ctx):
    quote = xnonbot_requests.get_quote()
    await ctx.respond(quote)


@gen.command(description="Gets a random waifu picture from https://waifu.pics/docs")
async def waifu(
    ctx,
    category: discord.Option(
        choices=xnonbot_requests.waifu_categories, description="Chose the category."
    ),
):
    waifu_pic = xnonbot_requests.get_waifu_pic(category)
    waifu_embed = discord.Embed(
        title="Waifu generated!",
        description=f"Here's a(n) {category} image for you.",
    )
    waifu_embed.set_image(url=waifu_pic)

    await ctx.respond(embed=waifu_embed)


@gen.command(description="Gets a random dog picture from https://dog.ceo/dog-api")
async def dog(ctx):
    dog = xnonbot_requests.get_dog_pic()
    dog_embed = discord.Embed(
        title="Bark!",
        description="Random dog picture generated.",
    )
    dog_embed.set_image(url=dog)

    await ctx.respond(embed=dog_embed)


@gen.command(description="Gets a random cat picture from https://thecatapi.com")
async def cat(ctx):
    cat = xnonbot_requests.get_cat_pic()
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
        image_output = xnonbot_requests.get_pexels_photos(search_query)

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
    would_you_rather = xnonbot_requests.get_would_you_rather()
    await ctx.respond(would_you_rather)


@gen.command(description="Generates a random dad joke.")
async def dadjoke(ctx):
    dad_joke = xnonbot_requests.get_dad_joke()
    await ctx.respond(dad_joke)


"""Game command group"""


@game.command(description="Chooses a random dice roll (1 to 6).")
async def roll(ctx):
    await ctx.respond(random.randint(1, 6))


@game.command(description="Plays a trivia game.")
async def trivia(
    ctx,
    category: discord.Option(
        choices=xnonbot_requests.trivia_categories,
        description="Select the category.",
    ),
    game_type: discord.Option(
        choices=["True or False", "Multiple answers"],
        description="Select the game type.",
    ),
):
    if game_type == "True or False":
        trivia_requests = xnonbot_requests.get_trivia_legacy(category)

        trivia_true_or_false_embed = discord.Embed(
            title=f"True or False Trivia", color=discord.Color.from_rgb(0, 217, 255)
        )
        trivia_true_or_false_embed.add_field(
            name="Question",
            value=f"{html.unescape(trivia_requests[0])} (The difficulty is {trivia_requests[1]}).\n\nAnswers in True or False!",
        )
        trivia_true_or_false_embed.set_footer(
            text=f"{category[0].upper() + category[1:]} trivia - Powered by opentdb.com"  # We want the category to start with a capital letter.
        )
        trivia_true_or_false_embed.set_thumbnail(url="attachment://opentdb.png")

        await ctx.respond(
            "You have 15 seconds to answer!",
            file=discord.File("local/opentriviadatabase.png", filename="opentdb.png"),
            embed=trivia_true_or_false_embed,
        )

        try:
            trivia_response = await bot.wait_for(  # Checks if the user responding is the same as the one requesting the initial interaction.
                "message",
                check=lambda message: message.author.id == ctx.author.id
                and message.channel.id == ctx.channel.id
                and message.content.lower()
                in [
                    "true",
                    "false",
                ],  # We want to ignore everything except "true" or "false".
                timeout=15,
            )
            if trivia_response.content.lower() == trivia_requests[2].lower():
                await ctx.send("You're correct!")
            else:
                await ctx.send(
                    f"Sorry, but the correct answer was {trivia_requests[2]}"
                )
        except asyncio.TimeoutError:
            await ctx.send(
                f"{ctx.user.mention} you have exceeded the time limit, please try again!"
            )

    elif game_type == "Multiple answers":
        trivia_requests = xnonbot_requests.get_trivia(category)
        answers_list = trivia_requests[3] + [trivia_requests[2]]
        random.shuffle(answers_list)

        answers_check = tuple(
            answer.lower() for answer in answers_list
        )  # Makes all the answers lowercase so then they become case-insensitive.

        trivia_multiple_answers_embed = discord.Embed(
            title=f"Multiple Answers Trivia", color=discord.Color.from_rgb(0, 217, 255)
        )
        trivia_multiple_answers_embed.add_field(
            name="Question",
            value=f"{html.unescape(trivia_requests[0])} (The difficulty is {trivia_requests[1]}).\n\n{answers_list[0]}, {answers_list[1]}, {answers_list[2]}, or {answers_list[3]}.",
        )
        trivia_multiple_answers_embed.set_footer(
            text=f"{category[0].upper() + category[1:]} trivia - Powered by opentdb.com"
        )
        trivia_multiple_answers_embed.set_thumbnail(url="attachment://opentdb.png")

        await ctx.respond(
            "You have 30 seconds to answer!",
            file=discord.File(
                "C:\Programming\XnonBot\local\opentriviadatabase.png",
                filename="opentdb.png",
            ),
            embed=trivia_multiple_answers_embed,
        )

        try:
            trivia_response = await bot.wait_for(
                "message",
                check=lambda message: message.author.id == ctx.author.id
                and message.channel.id == ctx.channel.id
                and message.content.lower() in answers_check,
                timeout=30,
            )
            if trivia_response.content.lower() == trivia_requests[2].lower():
                await ctx.send("You're correct!")
            else:
                await ctx.send(
                    f"Sorry, but the correct answer was {trivia_requests[2]}"
                )
        except asyncio.TimeoutError:
            await ctx.send(
                f"{ctx.user.mention} you have exceeded the time limit, please try again!"
            )


@game.command(description="Guess the number game.")
async def gtn(ctx, max: discord.Option(int, description="Maximum number to guess.")):
    random_number = random.randint(0, max)

    await ctx.respond(f"Guess the number (maximum: {max})")
    response = await bot.wait_for(
        "message", check=lambda message: message.author == ctx.author
    )  # Tells the bot to wait for a message, it must be sent by the same user.

    if int(response.content) == random_number:
        await ctx.send(f"you have guessed it right! The number is {random_number}.")
    elif int(response.content) > max:
        await ctx.send(f"That's too high! The max number is {max}.")
    else:
        return  # If the response message wasn't an integer.


@game.command(description="Plays rock, paper, scissors with the user.")
async def rps(
    ctx,
    choice: discord.Option(
        choices=["rock", "paper", "scissors"],
        description="Choose either rock, paper, or scissors.",
    ),
):
    rps_choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(rps_choices)

    if choice == bot_choice:
        output = "We tied!"
    elif choice == "rock" and bot_choice == "scissors":
        output = "You won!"
    elif choice == "paper" and bot_choice == "rock":
        output = "You won!"
    elif choice == "scissors" and bot_choice == "paper":
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


"""Wikipedia command group"""


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
                file=discord.File("local/wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_summary_embed,
            )  # If the bot can't send an interaction response for whatever reason.
        except:
            await ctx.send(
                file=discord.File(
                    "local/wikipedia.png",
                    filename="wikipedia.png",
                ),
                embed=wikipedia_summary_embed,
            )
    except wikipedia.DisambiguationError as e:
        options_list = str(option + ", " for option in e.options)

        exception_embed = discord.Embed(
            title="DisambiguationError, please specify your search query with the options below",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        exception_embed.add_field(name=f"{search} may refer to:", value=options_list)

        await ctx.respond(
            "Oops, an error occured!", embed=exception_embed, ephemeral=True
        )
    except Exception as e:
        await ctx.respond(e, ephemeral=True)


@wk.command(description="Searches for a link in Wikipedia")
async def link(ctx, query: discord.Option(str, description="The link to search for.")):
    await ctx.channel.trigger_typing()

    try:
        link_summary = wikipedia.summary(query, auto_suggest=False)
        search = (
            query.lower().replace(" ", "_").replace("  ", "_")
        )  # Removing empty space and instead replacing it with "_" so the url is valid.

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
                file=discord.File("local/wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_link_embed,
            )
        except:
            await ctx.send(
                file=discord.File("local/wikipedia.png", filename="wikipedia.png"),
                embed=wikipedia_link_embed,
            )
    except wikipedia.DisambiguationError as e:
        options_list = str(option + ", " for option in e.options)

        exception_embed = discord.Embed(
            title="DisambiguationError, please specify your search query with the options below",
            color=discord.Color.from_rgb(0, 217, 255),
        )
        exception_embed.add_field(name=f"{search} may refer to:", value=options_list)

        await ctx.respond(
            "Oops, an error occured!", embed=exception_embed, ephemeral=True
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
bot.add_application_command(gen)
bot.add_application_command(game)
bot.add_application_command(util)
bot.add_application_command(wk)

# Keep running the bot.
keep_alive.keep_alive()

# Actually running the bot.
bot.run(os.getenv("XNONBOTTOKEN"))
