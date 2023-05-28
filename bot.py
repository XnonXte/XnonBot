import discord
import random
import os
import html
from dotenv import load_dotenv
from BotModules import xnonbot_buttons, xnonbot_requests, keep_alive

load_dotenv("C:\Programming\XnonBot\.env")

version = "Beta 0.4.2"
prefix = ";"
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix=prefix, intents=intents)

# Command groups.
xb = discord.SlashCommandGroup("xnonbot", "general commands")
cfg = discord.SlashCommandGroup("config", "moderator only commands")

# Subgroups of the group xb.
gen = xb.create_subgroup("generate", "generate related command")
game = xb.create_subgroup("game", "game related commmands")
util = xb.create_subgroup("utility", "utilities related commands")
wk = xb.create_subgroup("wikipedia", "wikipedia related commands")

SLASHCOMMANDS = """
`quickstart` - Sends a quickstart message
`help` - Prompts help message
`github` - Github page for this bot
`about` - Sends information regarding this bot
`quote` - Sends a random inspirational quote
`roll` - Sends a random dice roll result, from 1 to 6
`rps` - Plays rock, paper, scissors with the user
`say` - Tell the bot to say something
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
"""

PREFIXEDCOMMANDS = """
`quickstart` - Sends a quickstart message
"""

CTXMENUS = """
`Join date` - Gets the join date for a user
`Created at` - Gets the creation date for a user
`Ping` - Ping a user
`Repeat` - Repeat a message 
"""

# snipped_message = None
# edited_message = None


# Startup.
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")


# Events that read message contents.
@bot.event
async def on_member_join(ctx, member):
    await ctx.respond(f"Please welcome {member.mention} to the server!")


# todo Make these lines of code working somehow.
# async def on_message_delete(message):
#     global snipped_author, snipped_message
#     snipped_message = f"Message: {message.content}"
#     snipped_author = f"Author: {message.author.id}"


# async def on_message_edit(before, after):
#     global old_message, edited_message, message_author
#     old_message = before.content
#     edited_message = after.content
#     message_author = after.author.id


"""Prefixed commands"""


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith(f"{prefix}quickstart"):
        await message.channel.send(
            f"Thank you for using XnonBot! You can start by prompting `/help` to get started."
        )


"""XnonBot command group"""


@xb.command(name="quickstart", description="Sends a quickstart message.")
async def quickstart(ctx):
    await ctx.respond(
        f"Thank you for using XnonBot! You can start by prompting `/help` to get started."
    )


@xb.command(description="Says hello to the user.")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.user.mention}!")


@xb.command(description="Overview of available slash commands.")
async def help(
    ctx,
    viewable: discord.Option(
        bool, description="Viewable to everyone.", required=False
    ),
):
    help_message_embed = discord.Embed(
        description="Thank you for using XnonBot! Created with 💖 by XnonXte.",
        color=discord.Colour.from_rgb(0, 217, 255),
    )
    help_message_embed.add_field(
        name="Commands", value=SLASHCOMMANDS, inline=False)
    help_message_embed.add_field(
        name="Prefixed commands", value=PREFIXEDCOMMANDS, inline=False
    )
    help_message_embed.add_field(
        name="Context menus", value=CTXMENUS, inline=False)

    help_message_embed.set_author(
        name="Help & About",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )
    help_message_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )
    help_message_embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png"
    )

    if viewable != True:
        ephemeral_message = False
    else:
        ephemeral_message = True

    await ctx.respond(
        embed=help_message_embed,
        view=xnonbot_buttons.HelpButtons(),
        ephemeral=ephemeral_message,
    )


@xb.command(description="Tells the bot to say something.")
async def say(ctx, message: discord.Option(str, description="Message to send.")):
    await ctx.respond(f"{ctx.user.mention} said: `{message}`")


@xb.command(description="Sends the information about this bot.")
async def about(ctx):
    await ctx.respond(
        "I'm a chat-bot developed by XnonXte! My code is available on GitHub (/github)."
    )


@xb.command(description="Official GitHub page for this bot.")
async def github(ctx):
    await ctx.respond("https://github.com/XnonXte/XnonBot")


"""Utility command subgroup"""


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


# todo Create a command to fetch a deleted message.
# @util.command(description="Gets a deleted message.")
# async def recentdelete(ctx):
#     if snipped_message is None:
#         await ctx.respond("There's no message to snipe!")
#     else:
#         await ctx.respond(f"{snipped_message}\n{snipped_author}")


# @util.command(description="Gets an edited message.")
# async def recentedit(ctx):
#     if edited_message is None:
#         await ctx.respond("There's no message edited!")
#     else:
#         await ctx.respond(
#             f"Old message: {old_message}\nEdited message:{edited_message}\nAuthor: {message_author} "
#         )

"""Generate command subgroup"""


@gen.command(description="Gets a random quote from zenquotes.io")
async def quote(ctx):
    quote = xnonbot_requests.get_quote()
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
    waifu_pic = xnonbot_requests.get_waifu_pic(category)
    if waifu_pic is None:
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return

    waifu_embed = discord.Embed(
        title="Waifu generated!",
        description=f"Here's a(n) {category} image for you.",
    )
    waifu_embed.set_image(url=waifu_pic)
    waifu_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )

    await ctx.respond(embed=waifu_embed)


@gen.command(description="Gets a random dog picture from https://dog.ceo/dog-api")
async def dog(ctx):
    dog = xnonbot_requests.get_dog_pic()
    dog_embed = discord.Embed(
        title="Bark!",
        description="Random dog picture generated.",
    )
    dog_embed.set_image(url=dog)
    dog_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )

    await ctx.respond(embed=dog_embed)


@gen.command(description="Gets a random cat picture from https://thecatapi.com")
async def cat(ctx):
    cat = xnonbot_requests.get_cat_pic()
    cat_embed = discord.Embed(
        title="Meow!",
        description="Random cat picture generated.",
    )
    cat_embed.set_image(url=cat)
    cat_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )

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
        pexels_output_embed.set_footer(
            text=f"XnonBot Version {version}",
            icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
        )

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


"""Game command subgroup"""


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
    trivia_question = xnonbot_requests.get_trivia(category.lower())
    if trivia_question is None:
        await ctx.respond("Invalid value, please try again!", ephemeral=True)
        return
    correct_trivia_answer = trivia_question[2]

    await ctx.respond(
        html.unescape(
            f"The difficulty is {trivia_question[1]} - {trivia_question[0]}")
    )

    await ctx.respond(
        f"Please select your answer!",
        view=xnonbot_buttons.TriviaButtons(ctx.author, correct_trivia_answer),
    )


@game.command(description="Guess the number game.")
async def gtn(ctx, max: discord.Option(int, description="Maximum number to guess.")):
    random_number = random.randint(0, max)

    await ctx.respond(f"Guess the number (maximum: {max})")
    response = await bot.wait_for(
        "message", check=lambda message: message.author == ctx.author
    )

    if int(response.content) == random_number:
        await ctx.send(f"You've guessed it right! The number is {random_number}.")
    elif int(response.content) > max:
        await ctx.send(f"That's too high! The max number is {max}.")
    else:
        return


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
    rps_embed.set_footer(
        text=f"XnonBot Version {version}",
        icon_url="https://cdn.discordapp.com/attachments/1103276522577596527/1111678075952971826/xnonbot.png",
    )

    await ctx.respond(embed=rps_embed)


"""Context menus"""


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


@bot.message_command(name="Repeat")
async def repeat(ctx, message: discord.Message):
    await ctx.respond(message.content)


"""Config command group"""  # Coming soon


# Add the groups we have created earlier to discord.
bot.add_application_command(xb)
bot.add_application_command(cfg)

# Running the bot.
# keep_alive.keep_alive()
bot.run(os.getenv("XNONBOTTOKEN"))
