import logging
from datetime import timedelta

import requests
from dynamic_preferences.registries import global_preferences_registry

from .baseScraper import BaseScraper
from .common import maybe_save_image
from ...models import *

global_preferences = global_preferences_registry.manager()


class EatSmarterScraper(BaseScraper):
    config_key = "eatsmarter"

    def work(self):
        categories = [(4161, 4), (4029, 3), (3857, 2), (3817, 1), (3855, 0)]
        for category in categories:
            self.set_index(0)
            self.set_max(100)
            while self.active and self.get_index() < self.get_max():
                self.scrape(self.get_index(), category)
                self.set_index(self.get_index() + 1)

    def create_recipe(self, recipe_json, recipe_type):
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
                "source": Recipe.Source.eatsmarter,
                "recipeType": recipe_type,
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
        maybe_save_image(recipe[0], image_url, 'scraper__Download_Recipe_Images')
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

    def scrape(self, index, category):
        headers = {"api-key": "c7f8ab363cdb3cd405cb41f79464d7b3d8089eab"}
        response = requests.request("GET",
                                    f"https://api.eatsmarter.de/v2/json/search/recipe?hs=8&sort=voting&page={index}&f[0]=field_secondary_recipe_category%3A{category[0]}",
                                    headers=headers)
        items = response.json()["results"]
        if len(items) == 0:
            self.set_max(index)
            return
        for recipeJson in items:
            try:
                recipe_id = recipeJson["id"]
                url = f"https://api.eatsmarter.de/v2/json/recipe/{recipe_id}"
                new_recipe_json = requests.get(url, headers=headers).json()
                temp = self.create_recipe(new_recipe_json, category[1])
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
                self.handle_scrape_error(e, f"Recipe with skip '{index}'")


s = EatSmarterScraper()


def get_scraper():
    global s
    return s
