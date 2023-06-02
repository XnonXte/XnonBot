import requests
import json
import os
from pexels_api import API
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\dev.env")

# The max list for choices in discord.Option is 25, we can't have all the categories sadly, I'm only putting 20 here.
waifu_categories = [
    "waifu",
    "neko",
    "megumin",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "pat",
    "smug",
    "bonk",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "slap",
    "kick",
    "happy",
    "wink",
    "dance",
]

# Only 10 for the time being.
trivia_categories = [
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


def get_quote():
    quote_response = requests.get("https://zenquotes.io/api/random")
    quote_convert_json = json.loads(quote_response.text)
    quote = quote_convert_json[0]["q"] + " -" + quote_convert_json[0]["a"]
    return quote


def get_dog_pic():
    dog_response = requests.get("https://dog.ceo/api/breeds/image/random")
    dog_convert_json = json.loads(dog_response.text)
    return dog_convert_json["message"]


def get_cat_pic():
    cat_response = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_convert_json = json.loads(cat_response.text)
    return cat_convert_json[0]["url"]


def get_waifu_pic(category):
    waifu_response = requests.get(f"https://api.waifu.pics/sfw/{category}")
    waifu_convert_json = json.loads(waifu_response.text)
    return waifu_convert_json["url"]


def get_trivia_legacy(category):
    available_category_true_or_false = {
        "animal": "https://opentdb.com/api.php?amount=1&category=27&type=boolean",
        "math": "https://opentdb.com/api.php?amount=1&category=19&type=boolean",
        "anime": "https://opentdb.com/api.php?amount=1&category=31&type=boolean",
        "history": "https://opentdb.com/api.php?amount=1&category=23&type=boolean",
        "geography": "https://opentdb.com/api.php?amount=1&category=22&type=boolean",
        "art": "https://opentdb.com/api.php?amount=1&category=25&type=boolean",
        "celebrity": "https://opentdb.com/api.php?amount=1&category=26&type=boolean",
        "computers": "https://opentdb.com/api.php?amount=1&category=18&type=boolean",
        "sports": "https://opentdb.com/api.php?amount=1&category=21&type=boolean",
        "cartoons": "https://opentdb.com/api.php?amount=1&category=32&type=boolean",
    }

    trivia_response = requests.get(available_category_true_or_false.get(category))
    trivia_convert_json = json.loads(trivia_response.text)
    return (
        trivia_convert_json["results"][0]["question"],
        trivia_convert_json["results"][0]["difficulty"],
        trivia_convert_json["results"][0]["correct_answer"],
    )


def get_trivia(category):
    available_category_multiple_answers = {
        "animal": "https://opentdb.com/api.php?amount=1&category=27&type=multiple",
        "math": "https://opentdb.com/api.php?amount=1&category=19&type=multiple",
        "anime": "https://opentdb.com/api.php?amount=1&category=31&type=multiple",
        "history": "https://opentdb.com/api.php?amount=1&category=23&type=multiple",
        "geography": "https://opentdb.com/api.php?amount=1&category=22&type=multiple",
        "art": "https://opentdb.com/api.php?amount=1&category=25&type=multiple",
        "celebrity": "https://opentdb.com/api.php?amount=1&category=26&type=multiple",
        "computers": "https://opentdb.com/api.php?amount=1&category=18&type=multiple",
        "sports": "https://opentdb.com/api.php?amount=1&category=21&type=multiple",
        "cartoons": "https://opentdb.com/api.php?amount=1&category=32&type=multiple",
    }

    trivia_response = requests.get(available_category_multiple_answers.get(category))
    trivia_convert_json = json.loads(trivia_response.text)
    return (
        trivia_convert_json["results"][0]["question"],
        trivia_convert_json["results"][0]["difficulty"],
        trivia_convert_json["results"][0]["correct_answer"],
        trivia_convert_json["results"][0]["incorrect_answers"],
    )


def get_pexels_photos(query):
    pexels_client_api = API(os.requests("PEXELSAPI"))
    pexels_client_api.search(query, page=1, results_per_page=1)
    images = pexels_client_api.get_entries()
    for i in images:
        return i.original


def get_dad_joke():
    dad_joke_requests = requests.get("https://icanhazdadjoke.com/slack")
    dad_joke_convert_json = json.loads(dad_joke_requests.text)
    return dad_joke_convert_json["attachments"][0]["text"]


def get_would_you_rather():
    wyr_requests = requests.get("https://would-you-rather-api.abaanshanid.repl.co/")
    wyr_convert_json = json.loads(wyr_requests.text)
    return wyr_convert_json["data"]
