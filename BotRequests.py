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
  dog_pic = dog_convert_json[
    "message"] + " random picture of dog has been generated!"
  return dog_pic

def get_cat_pic():
  cat_response = requests.get("https://api.thecatapi.com/v1/images/search")
  cat_convert_json = json.loads(cat_response.text)
  cat_pic = cat_convert_json[0][
    "url"] + " random picture of cat has been generated!"
  return cat_pic


def get_waifu_pic():
  waifu_response = requests.get         ("https://api.waifu.pics/sfw/waifu")
  waifu_convert_json = json.loads(waifu_response.text)
  waifu_pic = waifu_convert_json[
    "url"] + " random picture of waifu has been generated!"
  return waifu_pic


# Warning that it is NSFW, I will not be putting this into my bot. 
# def get_waifu_pic_nsfw():
#   waifu_nsfw_response = requests.get("https://api.waifu.pics/nsfw/waifu")
#   waifu_nsfw_convert_json = json.loads(waifu_nsfw_response.text)
#   waifu_nsfw_pic= waifu_nsfw_convert_json[
#     "url"] + " random picture of waifu has been generated!"
#   return waifu_nsfw_pic


def get_animal_trivia():
  animal_trivia_response = requests.get(
    "https://opentdb.com/api.php?amount=1&category=27&type=boolean")
  animal_trivia_convert_json = json.loads(animal_trivia_response.text)
  animal_trivia_question = animal_trivia_convert_json["results"][0]["question"]
  animal_trivia_difficulty = animal_trivia_convert_json["results"][0][
    "difficulty"]
  animal_trivia_correct_answer = animal_trivia_convert_json["results"][0][
    "correct_answer"]
  animal_trivia_incorrect_answer = animal_trivia_convert_json["results"][0][
    "incorrect_answers"]
  return animal_trivia_question, animal_trivia_difficulty, animal_trivia_correct_answer, animal_trivia_incorrect_answer


def get_math_trivia():
  math_trivia_response = requests.get(
    "https://opentdb.com/api.php?amount=1&category=19&type=boolean")
  trivia_convert_json = json.loads(math_trivia_response.text)
  math_trivia_question = trivia_convert_json["results"][0]["question"]
  math_trivia_difficulty = trivia_convert_json["results"][0]["difficulty"]
  math_trivia_correct_answer = trivia_convert_json["results"][0][
    "correct_answer"]
  math_trivia_incorrect_answer = trivia_convert_json["results"][0][
    "incorrect_answers"]
  return math_trivia_question, math_trivia_difficulty, math_trivia_correct_answer, math_trivia_incorrect_answer


def get_anime_trivia():
  anime_trivia_response = requests.get(
    "https://opentdb.com/api.php?amount=1&category=31&type=boolean")
  anime_trivia_convert_json = json.loads(anime_trivia_response.text)
  anime_trivia_question = anime_trivia_convert_json["results"][0]["question"]
  anime_trivia_difficulty = anime_trivia_convert_json["results"][0][
    "difficulty"]
  anime_trivia_correct_answer = anime_trivia_convert_json["results"][0][
    "correct_answer"]
  anime_trivia_incorrect_answer = anime_trivia_convert_json["results"][0][
    "incorrect_answers"]
  return anime_trivia_question, anime_trivia_difficulty, anime_trivia_correct_answer, anime_trivia_incorrect_answer


def get_pexels_photos(query):
  pexels_client_api = API(os.getenv("PEXELSAPI"))
  pexels_client_api.search(query, page=1, results_per_page=1)
  images = pexels_client_api.get_entries()
  for i in images:
    return i.photographer, i.url, i.original