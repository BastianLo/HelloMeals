import logging
import os
import threading
import uuid
from datetime import timedelta

import requests
from dynamic_preferences.registries import global_preferences_registry

from .common import get_image
from .scrapeConfig import scrapeConfig
from ...models import *

global_preferences = global_preferences_registry.manager()


# TODO: for scraper functionality:
# eg: functionality to redownload images (to improve quality)
# Possibly increase recipe quality compared to other images
class Scraper:
    def __init__(self):
        self.exception = None
        self.last_error = False
        self.limit = 50
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = scrapeConfig()
        self.active = False
        self.country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"

    def get_status(self):
        return {
            "max_recipes": self.config.ck_skip,
            "start_index": self.config.ck_index,
            "running": self.is_running(),
            "exception": self.exception
        }

    def work(self):
        r = requests.request("GET",
                             f"https://api.chefkoch.de/v2/search-gateway/recipes?tags=21&minimumRating={global_preferences['scraper__Chefkoch_Minimum_Rating']}&limit=0&offset=0")
        tags = self.create_all_tags(r.json()["tagGroups"])
        for tag in tags:
            self.config.set_ck_index(0)
            try:
                while (self.active and self.config.ck_index < self.config.ck_skip) or self.config.ck_index == 0:
                    self.scrape(self.config.ck_index, tag)
                    self.config.set_ck_index(self.config.ck_index + self.limit)
            except Exception as e:
                self.exception = str(e)
                self.active = False
                self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
                raise e

    def start(self):
        self.bearer_token = None
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
        self.config.set_ck_index(index)

    def restart(self):
        self.stop()
        self.config.set_ck_index(0)
        self.start()

    def is_running(self):
        return self.work_thread.is_alive()

    def create_recipe(self, recipe_json):
        if recipe_json["previewImageUrlTemplate"] is None or recipe_json["rating"] is None:
            return None
        image_url = recipe_json["previewImageUrlTemplate"].replace("<format>", "crop-720x480")
        if recipe_json["servings"] is None:
            return None
        recipe = Recipe.objects.update_or_create(
            helloFreshId=recipe_json["id"],
            defaults={
                "name": recipe_json["title"],
                "source": 3,
                # Todo: Get video link
                # "videoLink": recipe_json["videoLink"],
                "isExcludedFromIndex": not recipe_json["isIndexable"],
                "isPremium": recipe_json["isPremium"],
                "isPlus": recipe_json["isPlus"],
                "viewCount": recipe_json["viewCount"],
                "author": recipe_json["owner"]["id"],
                "headline": recipe_json["subtitle"],
                "websiteLink": recipe_json["siteUrl"],
                "prepTime": timedelta(minutes=recipe_json["preparationTime"]),
                "totalTime": timedelta(minutes=recipe_json["totalTime"]),
                "difficulty": recipe_json["difficulty"],
                "createdAt": recipe_json["createdAt"],
                "averageRating": recipe_json["rating"]["rating"],
                "ratingCount": recipe_json["rating"]["numVotes"],
                "servings": recipe_json["servings"],
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
                    "name": group_json["header"] if str(group_json["header"]).strip() != "" else None,
                }
            )[0]
            recipe.ingredient_groups.add(ingredient_group)
            recipe.save()
            for ingredient_json in group_json["ingredients"]:
                ingredient = Ingredient.objects.filter(name=ingredient_json["name"]).first()
                if ingredient is None:
                    ingredient = Ingredient.objects.update_or_create(
                        helloFreshId=ingredient_json["id"],
                        defaults={
                            "name": ingredient_json["name"],
                        }
                    )[0]
                # Create RecipeIngredient
                ingredient_id = ingredient_json["id"]
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=ingredient_id + ingredient_group.id,
                    defaults={
                        "ingredient_group": ingredient_group,
                        "ingredient": ingredient,
                        "amount": ingredient_json["amount"],
                        "unit": ingredient_json["unit"],
                    }
                )[0]

    def create_nutrients(self, recipe_json, recipe):
        if recipe_json["nutrition"] == None:
            return None
        nutrient_json = recipe_json["nutrition"]
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKj": None,
                "energyKcal": nutrient_json["kCalories"],
                "fat": nutrient_json["fatContent"],
                "fatSaturated": None,
                "carbs": nutrient_json["carbohydrateContent"],
                "sugar": None,
                "protein": nutrient_json["proteinContent"],
                "salt": None,
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_tags(self, recipe_json, recipe):
        for tag_json in recipe_json["fullTags"]:
            tag = Tag.objects.get(helloFreshId=tag_json["id"])
            if tag is None:
                continue
            try:
                recipe_tag = RecipeTag.objects.update_or_create(
                    id=recipe.helloFreshId + tag.helloFreshId,
                    defaults={
                        "recipe": recipe,
                        "tag": tag,
                    }
                )
            except:
                continue

    def create_work_steps(self, recipe_json, recipe):
        step = WorkSteps.objects.update_or_create(
            id=recipe.helloFreshId + "0",
            defaults={
                "relatedRecipe": recipe,
                "index": 0,
                "description": recipe_json["instructions"],
            }
        )[0]

    def create_all_tags(self, tag_groups):
        tags = []
        for tg in tag_groups:
            name = tg["key"].capitalize()
            tg_object, created = TagGroup.objects.get_or_create(name=name)
            for tag in tg["tags"]:
                Tag.objects.update_or_create(helloFreshId=tag["id"], name=tag["name"], type=tag["name"],
                                             tagGroup=tg_object)
                tags.append(tag["id"])
        return tags

    def scrape(self, index, tag):
        chefkoch_url = f"https://api.chefkoch.de/v2/search-gateway/recipes?tags=21,{tag}&minimumRating=4.2&limit={self.limit}&offset={index}"
        response = requests.request("GET", chefkoch_url)
        self.create_all_tags(response.json()["tagGroups"])
        items = response.json()["results"]
        self.config.set_ck_skip(min(response.json()["count"], 1000))
        for recipeJson in items:
            recipeJson = recipeJson["recipe"]
            try:
                recipe_id = recipeJson["id"]
                url = f"https://api.chefkoch.de/v2/recipes/{recipe_id}"
                new_recipe_json = requests.get(url).json()
                temp = self.create_recipe(new_recipe_json)
                if temp is None:
                    logging.warning(f"Skipping recipe with id {recipe_id} (index: {index})")
                    continue
                recipe, created = temp
                self.create_ingredients(new_recipe_json, recipe)
                self.create_nutrients(new_recipe_json, recipe)
                self.create_tags(new_recipe_json, recipe)
                self.create_work_steps(new_recipe_json, recipe)
                self.last_error = False
                if created:
                    logging.info(f"Successfully created recipe with id {recipe_id} (index: {index})")
                else:
                    logging.debug(f"Successfully updated recipe with id {recipe_id} (index: {index})")
            except Exception as e:
                print(self.last_error)
                if not self.last_error:
                    logging.warning(f"Recipe with skip '{index}' failed. Skipping... - Error: {e}")
                    self.last_error = True
                    raise e
                else:
                    logging.error(f"Recipe with skip '{index}' failed second time. Canceling")
                    raise e


s = Scraper()


def get_scraper():
    global s
    return s
