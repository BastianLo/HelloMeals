import os
import uuid
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from ...models import *
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
    return recipe


def create_ingredients(recipe_json, recipe):
    yields = recipe_json["yields"][-1]["ingredients"]
    for ingredient_json in recipe_json["ingredients"]:
        ingredient = Ingredient.objects.update_or_create(
            helloFreshId=ingredient_json["id"],
            defaults={
                "name": ingredient_json["name"]
            }
        )[0]
        if not (ingredient.image and ingredient.image.file):
            ingredient.image.save(str(uuid.uuid4()) + ".png", get_image(
                "https://img.hellofresh.com/q_40,w_480,f_auto,c_limit,fl_lossy/hellofresh_s3" + ingredient_json[
                    "imagePath"]))
        # Create RecipeIngredient
        ingredient_id = ingredient_json["id"]
        ingredient_yield = [y for y in yields if y["id"] == ingredient_id][0]
        recipe_ingredient = RecipeIngredient.objects.update_or_create(
            id=ingredient_id + recipe.helloFreshId,
            defaults={
                "recipe": recipe,
                "ingredient": ingredient,
                "amount": ingredient_yield["amount"],
                "unit": ingredient_yield["unit"],
            }
        )[0]


def create_utensil(recipe_json, recipe):
    for utensil_json in recipe_json["utensils"]:
        utensil = Utensil.objects.update_or_create(
            helloFreshId=utensil_json["id"],
            defaults={
                "name": utensil_json["name"],
                "type": utensil_json["type"],
            }
        )[0]
        recipe_utensil = RecipeUtensil.objects.update_or_create(
            id=recipe.helloFreshId + utensil.helloFreshId,
            defaults={
                "recipe": recipe,
                "utensil": utensil,
            }
        )


def create_nutrients(recipe_json, recipe):
    nutrient_json = recipe_json["nutrition"]
    nutrient = Nutrients.objects.update_or_create(
        id=recipe.helloFreshId + "nutrients",
        defaults={
            "energyKj": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530d"][0],
            "energyKcal": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305304"][0],
            "fat": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305307"][0],
            "fatSaturated": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305308"][0],
            "carbs": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305305"][0],
            "sugar": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305306"][0],
            "protein": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305309"][0],
            "salt": [n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530b"][0],
        }
    )[0]
    recipe.nutrients = nutrient
    recipe.save()


def create_cuisine(recipe_json, recipe):
    for cuisine_json in recipe_json["cuisines"]:
        cuisine = Cuisine.objects.update_or_create(
            helloFreshId=cuisine_json["id"],
            defaults={
                "name": cuisine_json["name"],
                "type": cuisine_json["type"],
            }
        )[0]
        recipe_cuisine = RecipeCuisine.objects.update_or_create(
            id=recipe.helloFreshId + cuisine.helloFreshId,
            defaults={
                "recipe": recipe,
                "cuisine": cuisine,
            }
        )


def create_tags(recipe_json, recipe):
    for tag_json in recipe_json["tags"]:
        tag = Tag.objects.update_or_create(
            helloFreshId=tag_json["id"],
            defaults={
                "name": tag_json["name"],
                "type": tag_json["type"],
            }
        )[0]
        recipe_tag = RecipeTag.objects.update_or_create(
            id=recipe.helloFreshId + tag.helloFreshId,
            defaults={
                "recipe": recipe,
                "tag": tag,
            }
        )


def scrape(index):
    headers = {
        'authorization': f'Bearer {bearer()}',
    }
    response = requests.request("GET", HELLO_FRESH_URL + str(index), headers=headers)
    items = response.json()["items"]

    for recipeJson in items:
        recipe = create_recipe(recipeJson)
        create_ingredients(recipeJson, recipe)
        create_utensil(recipeJson, recipe)
        create_nutrients(recipeJson, recipe)
        create_cuisine(recipeJson, recipe)
        create_tags(recipeJson, recipe)
