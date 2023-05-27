import requests
import json
import os
from pexels_api import API
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\.env")

waifu_tuple = (
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
trivia_list = [
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
    if category not in waifu_tuple:
        return None

    waifu_response = requests.get(f"https://api.waifu.pics/sfw/{category}")
    waifu_convert_json = json.loads(waifu_response.text)
    return waifu_convert_json["url"]


def get_trivia(category):
    if category not in trivia_list:
        return None

    available_category = {
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
    trivia_response = requests.get(available_category.get(category))
    trivia_convert_json = json.loads(trivia_response.text)
    trivia_question = trivia_convert_json["results"][0]["question"]
    trivia_difficulty = trivia_convert_json["results"][0]["difficulty"]
    trivia_correct_answer = trivia_convert_json["results"][0]["correct_answer"]
    return trivia_question, trivia_difficulty, trivia_correct_answer


def get_pexels_photos(query):
    pexels_client_api = API(os.environ["PEXELSAPI"])
    pexels_client_api.search(query, page=1, results_per_page=1)
    images = pexels_client_api.get_entries()
    for i in images:
        return i.original