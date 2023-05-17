# Option template for interactions.py
    # name="COMMAND_NAME",
    # description="DESCRIPTION",
    # options=[
    #     Option(
    #     type=OptionType.TYPE,
    #     name="OPTIONNAME",
    #     description="OPTIONDESCRIPTION",
    #     required=BOOL,
    #     ),
    # ],

# Button template for interactions.py
        # style=ButtonStyle.TYPE,
        # custom_id="IDHERE",
        # label="LABELHERE",

# Option template for interaction.py
        # custom_id="IDHERE",
        # options=[
        #     SelectOption(label="Option 1", value="option-1"),
        #     SelectOption(label="Option 2", value="option-2")
        # ],
        # placeholder="PLACEHOLDER",

# XnonBot Version Beta 0.3
import interactions
import os
import html
import random
import BotRequests
from dotenv import load_dotenv
from interactions import Option, OptionType, CommandContext # Modules that we want

load_dotenv("C:\Programming\XnonBot\dev.env")
bot = interactions.Client(token=os.getenv("TESTINGBOTTOKEN"))

commands = """
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


@bot.event
async def on_ready():
    print("The bot is up!")


@bot.command(name="hello", description="Say hello to the user.")
async def hello(ctx: CommandContext):
    await ctx.send(f"Hello {ctx.user.mention}!")


@bot.command(name="help", description="Send a list of available slash commands.")
async def help(ctx: CommandContext):
    await ctx.send(commands)


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


@bot.command(name="quote", description="Get a random waifu picture.")
async def quote(ctx: CommandContext):
    quote = BotRequests.get_quote()
    await ctx.send(quote)


@bot.command(name="waifu", description="Get a random waifu picture.")
async def waifu(ctx: CommandContext):
    waifu = BotRequests.get_waifu_pic()
    await ctx.send(waifu)


@bot.command(name="dog", description="Get a random waifu picture.")
async def dog(ctx: CommandContext):
    dog = BotRequests.get_dog_pic()
    await ctx.send(dog)


@bot.command(name="cat", description="Get a random waifu picture.")
async def cat(ctx: CommandContext):
    cat = BotRequests.get_cat_pic()
    await ctx.send(cat)

    
@bot.command(
    name="rps",
    description="Play rock, paper, scissors with the user",
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
            'Invalid choice. Please choose either rock, paper, or scissors!',
            ephemeral=True)
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
  await ctx.send(
    f"An image of {search_query} has been generated! Photographed by: {image_output[0]}, original link: {image_output[2]} - Powered by pexels.com"
  )


@bot.event
async def on_message(message):

  def check_message(initial_requests):
    return initial_requests.author == message.author and initial_requests.channel == message.channel and initial_requests.content.lower(
    ) in ["true", "false"]

  if message.content.startswith("$help"):
    await message.channel.send(commands)

  if message.content.startswith("$animaltrivia"):
    animal_trivia = BotRequests.get_animal_trivia()
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
    math_trivia = BotRequests.get_math_trivia()
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
    anime_trivia = BotRequests.get_anime_trivia()
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


bot.start()


