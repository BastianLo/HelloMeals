import os
import uuid
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from ...models import Recipe
from isodate import parse_duration
from django.core.files.base import File

country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"
HELLO_FRESH_URL = f"https://www.hellofresh.de/gw/api/recipes?country={country}&order=-favorites&take=1&skip="

bearer_token = None


def bearer():
    global bearer_token
    if bearer_token is not None:
        return bearer_token
    url = "https://www.hellofresh.de"
    html = requests.get(url)
    token = html.text[html.text.index("access_token"):]
    token = token[token.index(":") + 2:]
    token = token[:token.index('"')]
    bearer_token = token
    return bearer_token


def get_image(url):
    img_tmp = NamedTemporaryFile(delete=True)
    with urlopen(url) as uo:
        assert uo.status == 200
        img_tmp.write(uo.read())
        img_tmp.flush()
    img = File(img_tmp)
    return img


def create_recipe(recipe_json):
    recipe = Recipe.objects.update_or_create(
        helloFreshId=recipe_json["id"],
        defaults={
            "name": recipe_json["name"],
            "headline": recipe_json["headline"],
            "description": recipe_json["description"],
            "cardLink": recipe_json["cardLink"],
            "websiteLink": recipe_json["canonicalLink"],
            "prepTime": parse_duration(recipe_json["prepTime"]) if recipe_json["prepTime"] else None,
            "totalTime": parse_duration(recipe_json["totalTime"]) if recipe_json["totalTime"] else None,
            "difficulty": recipe_json["difficulty"],
            "createdAt": recipe_json["createdAt"],
            "updatedAt": recipe_json["updatedAt"],
            "favoritesCount": recipe_json["favoritesCount"],
            "averageRating": recipe_json["averageRating"],
            "ratingCount": recipe_json["ratingsCount"],
            "servings": recipe_json["yields"][-1]["yields"],
        }
    )[0]
    if not (recipe.image and recipe.image.file):
        recipe.image.save(str(uuid.uuid4()) + ".png", get_image(
            "https://img.hellofresh.com/q_40,w_720,f_auto,c_limit,fl_lossy/hellofresh_s3" + recipe_json[
                "imagePath"]))


def scrape(index):
    headers = {
        'authorization': f'Bearer {bearer()}',
    }
    response = requests.request("GET", HELLO_FRESH_URL + str(index), headers=headers)
    items = response.json()["items"]

    for recipeJson in items:
        create_recipe(recipeJson)
