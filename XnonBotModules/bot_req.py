import requests
import json
import os
from pexels_api import API
from dotenv import load_dotenv

load_dotenv("C:\Programming\XnonBot\dev.env")


def get_quote():
    quote_response = requests.get("https://zenquotes.io/api/random")
    quote_convert_json = json.loads(quote_response.text)
    quote = quote_convert_json[0]["q"] + " -" + quote_convert_json[0]["a"]
    return quote


def get_dog_pic():
    dog_response = requests.get("https://dog.ceo/api/breeds/image/random")
    dog_convert_json = json.loads(dog_response.text)
    dog_pic = "Here's a random picture of dog for you! " + dog_convert_json["message"]
    return dog_pic


def get_cat_pic():
    cat_response = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_convert_json = json.loads(cat_response.text)
    cat_pic = "Here's a random picture of cat for you! " + cat_convert_json[0]["url"]
    return cat_pic


def get_waifu_pic(arg):
    waifu_response = requests.get(f"https://api.waifu.pics/sfw/{arg}")
    waifu_convert_json = json.loads(waifu_response.text)
    waifu_pic = f" Here's a random {arg} picture for you! " + waifu_convert_json["url"]
    return waifu_pic


def get_trivia(arg):
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
    trivia_response = requests.get(available_category.get(arg))
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
        return i.photographer, i.url, i.original
