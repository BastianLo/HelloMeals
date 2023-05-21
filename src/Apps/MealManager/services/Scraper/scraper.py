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


def scrape():
    for i in range(1):
        headers = {
            'authorization': f'Bearer {bearer()}',
        }

        response = requests.request("GET", HELLO_FRESH_URL + str(i), headers=headers)

        items = response.json()["items"]

        for recipeJson in items:
            recipe = Recipe.objects.update_or_create(
                helloFreshId=recipeJson["id"],
                defaults={
                    "name": recipeJson["name"],
                    "headline": recipeJson["headline"],
                    "description": recipeJson["description"],
                    "cardLink": recipeJson["cardLink"],
                    "websiteLink": recipeJson["canonicalLink"],
                    "prepTime": parse_duration(recipeJson["prepTime"]) if recipeJson["prepTime"] else None,
                    "totalTime": parse_duration(recipeJson["totalTime"]) if recipeJson["totalTime"] else None,
                    "difficulty": recipeJson["difficulty"],
                    "createdAt": recipeJson["createdAt"],
                    "updatedAt": recipeJson["updatedAt"],
                    "favoritesCount": recipeJson["favoritesCount"],
                    "averageRating": recipeJson["averageRating"],
                    "ratingCount": recipeJson["ratingsCount"],
                    "servings": recipeJson["yields"][-1]["yields"],
                }
            )[0]
            if not (recipe.image and recipe.image.file):
                recipe.image.save(str(uuid.uuid4()) + ".png",get_image(
                    "https://img.hellofresh.com/q_40,w_720,f_auto,c_limit,fl_lossy/hellofresh_s3" + recipeJson[
                        "imagePath"]))
