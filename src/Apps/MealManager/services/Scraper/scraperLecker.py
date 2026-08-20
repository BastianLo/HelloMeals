import logging
import re

import requests
from dynamic_preferences.registries import global_preferences_registry
from isodate import parse_duration

from .baseScraper import BaseScraper
from .common import maybe_save_image, is_valid_iso_duration
from ...models import *

global_preferences = global_preferences_registry.manager()


def extract_servings(recipe_yield):
    """Lecker's recipeYield is free text like "4 Personen", not a plain number."""
    if recipe_yield is None:
        return None
    match = re.search(r"\d+", str(recipe_yield))
    return int(match.group(0)) if match else None


class Scraper(BaseScraper):
    config_key = "lecker"

    def __init__(self):
        super().__init__()
        self.limit = 20

    def work(self):
        while self.active and self.get_index() < self.get_max():
            self.scrape(self.get_index())
            self.set_index(self.get_index() + self.limit)

    def create_recipe(self, recipe_json, url, id):
        paragraphs = recipe_json["body"]["paragraphs"]
        image_paragraph = [p for p in paragraphs if p["paragraphType"] == "image"]
        if len(image_paragraph) != 1 or image_paragraph[0]["image"] is None:
            return None
        image_url = f"https://images.lecker.de/id={image_paragraph[0]['image']['imageId']},b=lecker,w=720,rm=sk.webp"
        recipe_paragraph = [p for p in recipe_json["metaData"]["structuredData"] if p["@type"] == "Recipe"][0]
        d = recipe_json["metaData"]["teaser"]["difficultyText"]
        difficulty = 1 if d == "ganz einfach" else 1 if d == "einfach" else 2 if d == "fortgeschritten" else None
        if difficulty is None:
            raise Exception("Difficulty not found " + d)
        recipe = Recipe.objects.update_or_create(
            helloFreshId=id,
            defaults={
                "name": recipe_paragraph["name"],
                "description": recipe_paragraph["description"],
                "source": Recipe.Source.lecker,
                "websiteLink": url,
                "prepTime": parse_duration(recipe_paragraph["cookTime"]) if recipe_paragraph[
                                                                                "cookTime"] and is_valid_iso_duration(
                    recipe_paragraph["cookTime"]) and recipe_paragraph["cookTime"] != "0" else None,
                "totalTime": parse_duration(recipe_paragraph["totalTime"]) if recipe_paragraph[
                                                                                  "totalTime"] and is_valid_iso_duration(
                    recipe_paragraph["totalTime"]) and recipe_paragraph["totalTime"] != "0" else None,
                "difficulty": difficulty,
                "createdAt": recipe_paragraph["datePublished"] if "datePublished" in recipe_paragraph else None,
                "updatedAt": recipe_paragraph["dateModified"] if "dateModified" in recipe_paragraph else None,

                "averageRating": recipe_paragraph["aggregateRating"][
                    "ratingValue"] if "aggregateRating" in recipe_paragraph else 0,
                "ratingCount": recipe_paragraph["aggregateRating"][
                    "ratingCount"] if "aggregateRating" in recipe_paragraph else 0,
                "servings": extract_servings(recipe_paragraph.get("recipeYield")),
                "HelloFreshImageUrl": image_url
            }
        )
        maybe_save_image(recipe[0], image_url, 'scraper__Download_Recipe_Images')
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        for i, group_json in enumerate(recipe_json["ingredientGroups"]):
            ingredient_group = IngredientGroup.objects.update_or_create(
                id=recipe.helloFreshId + str(i),
                defaults={
                    "name": None,
                }
            )[0]
            recipe.ingredient_groups.add(ingredient_group)
            recipe.save()
            for ingredient_json in group_json["ingredients"]:
                ingredient = Ingredient.objects.filter(name=ingredient_json["ingredientName"]).first()
                if ingredient is None:
                    ingredient = Ingredient.objects.update_or_create(
                        helloFreshId=str(uuid.uuid4()),
                        defaults={
                            "name": ingredient_json["ingredientName"],
                        }
                    )[0]
                # Create RecipeIngredient
                ingredient_id = ingredient.helloFreshId
                if "quantity" in ingredient_json:
                    reunit = re.search(r"(\d+)", ingredient_json["quantity"], re.IGNORECASE)
                    if reunit:
                        unit = reunit.group(
                            1)
                    else:
                        unit = None
                else:
                    unit = None
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=ingredient_id + ingredient_group.id,
                    defaults={
                        "ingredient_group": ingredient_group,
                        "ingredient": ingredient,
                        "amount": unit,
                        "unit": ingredient_json["unit"] if "unit" in ingredient_json else None,
                    }
                )[0]

    def create_nutrients(self, recipe_json, recipe):
        if recipe_json["nutritionFacts"] == None:
            return None
        nutrient_json = recipe_json["nutritionFacts"]
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKcal": nutrient_json["calories"] if "calories" in nutrient_json else None,
                "protein": nutrient_json["protein"] if "protein" in nutrient_json else None,
                "carbs": nutrient_json["carbohydrate"] if "carbohydrate" in nutrient_json else None,
                "fat": nutrient_json["fat"] if "fat" in nutrient_json else None,
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_work_steps(self, recipe_json, recipe):
        i = 0
        for ig in recipe_json["instructionGroups"]:
            for step_json in ig["instructions"]:
                step = WorkSteps.objects.update_or_create(
                    id=recipe.helloFreshId + str(i),
                    defaults={
                        "relatedRecipe": recipe,
                        "index": i,
                        "description": step_json["step"]["plain"],
                    }
                )[0]
                i += 1

    def scrape(self, index):
        list_url = f"https://proxy.xceler8.io/v2/search?brand=lecker&q=(documentData.paragraphs.recipe.category:%22Hauptgericht%22)&offset={index}&limit={self.limit}&type=article"
        response = requests.request("GET", list_url)
        items = response.json()["results"]
        self.set_max(response.json()["total"])
        for recipeJson in items:
            try:
                url = f"https://proxy.xceler8.io/v2/page/lecker?url=%2F{recipeJson['url'].replace('/', '')}"
                new_recipe_json = requests.get(url, headers={
                    "x-api-key": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYXBpS2V5IiwidGVuYW50IjoiQlhLSERFIiwiYnJhbmQiOiJsZWNrZXIiLCJpYXQiOjE1MTMwOTAyMzEsImV4cCI6NDY2NjY5MDIzMX0.w_2sciFgg7Sk5WZmsv5cl-tg9RLPOyy3CZIxvwKqrkw"}).json()
                temp = self.create_recipe(new_recipe_json, "https://lecker.de" + recipeJson['url'],
                                          recipeJson['assetId'])
                if temp is None:
                    logging.warning(f"Skipping recipe with url {url} (index: {index})")
                    continue
                recipe, created = temp
                recipe_paragraph = [p for p in new_recipe_json["body"]["paragraphs"] if p["paragraphType"] == "recipe"][
                    0]["recipe"]
                self.create_ingredients(recipe_paragraph, recipe)
                self.create_nutrients(recipe_paragraph, recipe)
                self.create_work_steps(recipe_paragraph, recipe)
                self.last_error = False
                if created:
                    logging.info(f"Successfully created recipe with id {recipe.helloFreshId} (index: {index})")
                else:
                    logging.debug(f"Successfully updated recipe with id {recipe.helloFreshId} (index: {index})")
            except Exception as e:
                self.handle_scrape_error(e, f"Recipe with skip '{index}'")


s = Scraper()


def get_scraper():
    global s
    return s
