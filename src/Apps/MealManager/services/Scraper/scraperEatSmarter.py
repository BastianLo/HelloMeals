import logging
import threading
import uuid
from datetime import timedelta

import requests
from dynamic_preferences.registries import global_preferences_registry

from .common import get_image
from .scrapeConfig import scrapeConfig
from ...models import *

global_preferences = global_preferences_registry.manager()


class KSScraper:
    def __init__(self):
        self.exception = None
        self.last_error = False
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = scrapeConfig()
        self.active = False

    def get_status(self):
        return {
            "max": self.config.es_max,
            "index": self.config.es_index,
            "running": self.is_running(),
            "exception": self.exception
        }

    def work(self):
        try:
            while self.active and self.config.es_index < self.config.es_max:
                self.scrape(self.config.es_index)
                self.config.set_es_index(self.config.es_index + 1)
        except Exception as e:
            self.exception = str(e)
            self.active = False
            self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
            raise e

    def start(self):
        self.exception = None
        self.active = True
        if self.is_running():
            return
        self.work_thread.start()

    def stop(self):
        if not self.active:
            return
        self.active = False
        self.work_thread.join()
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)

    def set_progress(self, index):
        self.config.set_es_index(index)

    def restart(self):
        self.stop()
        self.config.set_es_index(1)
        self.start()

    def is_running(self):
        return self.work_thread.is_alive()

    def create_recipe(self, recipe_json):
        if recipe_json["title"] is None:
            return None
        image_url = recipe_json["image"]["url"]
        difficulty = 1 if recipe_json["difficulty"] == "leicht" else 2 if recipe_json[
                                                                              "difficulty"] == "mittel" else 3 if \
            recipe_json["difficulty"] == "schwer" else 3 if recipe_json["difficulty"] == "anspruchsvoll" else None
        if difficulty is None:
            raise Exception("Difficulty not found: " + recipe_json["difficulty"])

        recipe = Recipe.objects.update_or_create(
            helloFreshId="es" + str(recipe_json["id"]),
            defaults={
                "name": recipe_json["title"],
                "source": 5,
                "recipeType": 0,
                "healthScore": recipe_json["healthScore"],
                "isPremium": recipe_json["isPremium"],
                "headline": recipe_json["subtitle"],
                "description": recipe_json["whyHealthy"] if "whyHealthy" in recipe_json else None,
                "websiteLink": "https://eatsmarter.de" + recipe_json["url"],
                "prepTime": timedelta(minutes=recipe_json["preparationTime"]["minutes"]),
                "totalTime": timedelta(minutes=recipe_json["preparationTime"]["minutesInclWait"]),
                "difficulty": difficulty,
                "averageRating": recipe_json["rating"]["average"],
                "ratingCount": recipe_json["rating"]["count"],
                "servings": recipe_json["servings"]["measurement"],
                "HelloFreshImageUrl": image_url
            }
        )
        if (not (recipe[0].image and recipe[0].image.file)) and global_preferences['scraper__Download_Recipe_Images']:
            image = get_image(image_url)
            if image is not None:
                recipe[0].image.save(str(uuid.uuid4()) + ".png", image)
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        for i, group_json in enumerate(recipe_json["ingredientGroups"]):
            ingredient_group = IngredientGroup.objects.update_or_create(
                id=recipe.helloFreshId + str(i),
                defaults={
                    "name": group_json["name"],
                }
            )[0]
            recipe.ingredient_groups.add(ingredient_group)
            recipe.save()
            for ingredient_json in group_json["ingredients"]:
                if ingredient_json["namePlural"] is None:
                    continue
                ingredient = Ingredient.objects.update_or_create(
                    helloFreshId="es" + str(ingredient_json["id"]),
                    defaults={
                        "name": ingredient_json["namePlural"],
                    }
                )[0]
                # Create RecipeIngredient
                ingredient_id = ingredient.helloFreshId
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=str(ingredient_id) + str(ingredient_group.id),
                    defaults={
                        "ingredient_group": ingredient_group,
                        "ingredient": ingredient,
                        "amount": ingredient_json["amount"],
                        "unit": ingredient_json["unit"],
                    }
                )[0]

    def create_utensil(self, recipe_json, recipe):
        for utensil_string in recipe_json["kitchenUtensils"]:
            utensil_id = utensil_string.replace(" ", "")
            utensil = Utensil.objects.update_or_create(
                helloFreshId=utensil_id,
                defaults={
                    "name": utensil_string,
                }
            )[0]
            recipe_utensil = RecipeUtensil.objects.update_or_create(
                id=recipe.helloFreshId + utensil.helloFreshId,
                defaults={
                    "recipe": recipe,
                    "utensil": utensil,
                }
            )

    def create_nutrients(self, recipe_json, recipe):
        nutrient_json = recipe_json["nutritionalValues"]
        calories = None
        protein = None
        fat = None
        carbs = None
        sugar = None
        for n in nutrient_json:
            if n["label"] == "Kalorien":
                calories = n["value"]
            if n["label"] == "Protein":
                protein = n["value"]
            if n["label"] == "Fett":
                fat = n["value"]
            if n["label"] == "Kohlenhydrate":
                carbs = n["value"]
            if n["label"] == "zugesetzter Zucker":
                sugar = n["value"]
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKcal": calories,
                "fat": fat,
                "carbs": carbs,
                "sugar": sugar,
                "protein": protein,
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_work_steps(self, recipe_json, recipe):
        for i, step_json in enumerate(recipe_json["preparationSteps"]):
            step = WorkSteps.objects.update_or_create(
                id=recipe.helloFreshId + str(i),
                defaults={
                    "relatedRecipe": recipe,
                    "index": i,
                    "description": step_json["text"],
                }
            )[0]

    def scrape(self, index):
        headers = {"api-key": "c7f8ab363cdb3cd405cb41f79464d7b3d8089eab"}
        response = requests.request("GET",
                                    f"https://api.eatsmarter.de/v2/json/search/recipe?hs=8&sort=voting&page={index}&f[0]=field_secondary_recipe_category%3A3855",
                                    headers=headers)
        items = response.json()["results"]
        if len(items) == 0:
            self.config.set_es_max(index)
            return
        for recipeJson in items:
            try:
                recipe_id = recipeJson["id"]
                url = f"https://api.eatsmarter.de/v2/json/recipe/{recipe_id}"
                new_recipe_json = requests.get(url, headers=headers).json()
                temp = self.create_recipe(new_recipe_json)
                if temp is None:
                    logging.warning(f"Skipping recipe with id {new_recipe_json['id']} (index: {index})")
                    continue
                recipe, created = temp
                self.create_ingredients(new_recipe_json, recipe)
                self.create_utensil(new_recipe_json, recipe)
                self.create_nutrients(new_recipe_json, recipe)
                self.create_work_steps(new_recipe_json, recipe)
                self.last_error = False
                if created:
                    logging.info(f"Successfully created recipe with id {new_recipe_json['id']} (index: {index})")
                else:
                    logging.debug(f"Successfully updated recipe with id {new_recipe_json['id']} (index: {index})")
            except Exception as e:
                if not self.last_error:
                    logging.warning(f"Recipe with skip '{index}' failed. Skipping... - Error: {e}")
                    self.last_error = True
                    raise e
                else:
                    logging.error(f"Recipe with skip '{index}' failed second time. Canceling")
                    raise e


s = KSScraper()


def get_scraper():
    global s
    return s
