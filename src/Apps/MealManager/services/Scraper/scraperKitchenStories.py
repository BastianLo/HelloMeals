import logging
import os
import re
import threading
import uuid
from datetime import timedelta
from io import BytesIO
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from PIL import Image
from django.core.files.base import File
from dynamic_preferences.registries import global_preferences_registry

from .scrapeConfig import scrapeConfig
from ...models import *

global_preferences = global_preferences_registry.manager()


def is_valid_iso_duration(duration_str):
    pattern = r'^P(?:\d+Y)?(?:\d+M)?(?:\d+W)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$'
    return re.match(pattern, duration_str) is not None


class KSScraper:
    def __init__(self):
        self.PAGE_SIZE = 10
        self.country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"
        self.exception = None
        self.last_error = False
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = scrapeConfig()
        self.active = False

    def get_status(self):
        return {
            "max_page": self.config.ks_max_page,
            "page": self.config.ks_page,
            "running": self.is_running(),
            "exception": self.exception
        }

    def work(self):
        try:
            while self.active and self.config.ks_page < self.config.ks_max_page:
                self.scrape(self.config.ks_page)
                self.config.set_ks_page(self.config.ks_page + 1)
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
        self.config.set_ks_page(index)

    def restart(self):
        self.stop()
        self.config.set_ks_page(1)
        self.start()

    def is_running(self):
        return self.work_thread.is_alive()

    def get_image(self, url):
        if url is None:
            return None

        try:
            with urlopen(url) as uo:
                assert uo.status == 200
                image_data = uo.read()

            # Open the image using Pillow
            image = Image.open(BytesIO(image_data))

            # Resize the image
            max_width = 720
            if image.width > max_width:
                ratio = max_width / float(image.width)
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.ANTIALIAS)

            # Save the resized image to a temporary file
            img_tmp = NamedTemporaryFile(delete=True)
            image.save(img_tmp, format='JPEG')

            # Create a Django File object from the temporary file
            img = File(img_tmp)

            return img
        except:
            return None

    def create_recipe(self, recipe_json):
        if "tags" not in recipe_json or "amount" not in recipe_json["servings"] or "duration" not in recipe_json:
            return None
        # Skip recipes that are not main recipes:
        if len([tag for tag in recipe_json["tags"] if tag["id"] == "f622a099-d5c2-4db2-a689-e7f856db38a8"]) == 0:
            logging.info(f"Skipping recipe {recipe_json['id']} because recipe is not main")
            return None
        if "image" not in recipe_json or recipe_json["image"]["url"] is None:
            return None
        image_url = recipe_json["image"]["url"]
        recipe = Recipe.objects.update_or_create(
            helloFreshId=recipe_json["id"],
            defaults={
                "name": recipe_json["title"],
                "source": 2,
                "clonedFrom": None,
                "videoLink": None,
                "highlighted": None,
                "isAddon": None,
                "isDinnerToLunch": None,
                "isExcludedFromIndex": None,
                "isPremium": None,
                "author": recipe_json["author"]["id"],
                "helloFreshActive": None,
                "headline": None,
                "description": recipe_json["chefs_note"] if "chefs_note" in recipe_json else None,
                "cardLink": None,
                "websiteLink": recipe_json["url"],
                "prepTime": timedelta(minutes=recipe_json["duration"]["preparation"]),
                "totalTime": timedelta(
                    minutes=recipe_json["duration"]["preparation"] + recipe_json["duration"]["resting"]),
                "difficulty": 1 if recipe_json["difficulty"] == "easy" else 2 if recipe_json[
                                                                                     "difficulty"] == "medium" else 3 if
                recipe_json["difficulty"] == "hard" else None,
                "createdAt": recipe_json["publishing"]["created"],
                "updatedAt": recipe_json["publishing"]["updated"],
                "favoritesCount": recipe_json["user_reactions"]["like_count"],
                "averageRating": recipe_json["user_reactions"]["rating"] * 5,
                "ratingCount": recipe_json["user_reactions"]["rating_count"],
                "servings": recipe_json["servings"]["amount"],
                "HelloFreshImageUrl": image_url
            }
        )
        if (not (recipe[0].image and recipe[0].image.file)) and global_preferences['scraper__Download_Recipe_Images']:
            image = self.get_image(image_url)
            if image is not None:
                recipe[0].image.save(str(uuid.uuid4()) + ".png", image)
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        for ingredient_block in recipe_json["ingredients"]:
            for ingredient_json in ingredient_block["list"]:
                ingredient_id = ingredient_json["id"] if "id" in ingredient_json else str(
                    hash(ingredient_json["name"]["rendered"]))
                ingredient = Ingredient.objects.update_or_create(
                    helloFreshId=ingredient_id,
                    defaults={
                        "name": ingredient_json["name"]["rendered"],
                    }
                )[0]
                # Create RecipeIngredient
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=ingredient_id + recipe.helloFreshId,
                    defaults={
                        "recipe": recipe,
                        "ingredient": ingredient,
                        "amount": ingredient_json["measurement"]["metric"][
                            "amount"] if "measurement" in ingredient_json and "metric" in ingredient_json[
                            "measurement"] and "amount" in ingredient_json["measurement"]["metric"] else None,
                        "unit": ingredient_json["measurement"]["metric"]["unit"]["name"][
                            "rendered"] if "measurement" in ingredient_json and "unit" in
                                           ingredient_json["measurement"]["metric"] else None,
                    }
                )[0]

    def create_utensil(self, recipe_json, recipe):
        if "utensils" not in recipe_json:
            return None
        for utensil_json in recipe_json["utensils"]:
            utensil_id = utensil_json["id"] if "id" in utensil_json else str(
                hash(utensil_json["name"]["rendered"]))
            utensil = Utensil.objects.update_or_create(
                helloFreshId=utensil_id,
                defaults={
                    "name": utensil_json["name"]["rendered"],
                    "type": None,
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
        if "nutrition" not in recipe_json:
            return None
        nutrient_json = recipe_json["nutrition"]
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKj": None,
                "energyKcal": nutrient_json["calories"],
                "fat": nutrient_json["fat"],
                "fatSaturated": None,
                "carbs": nutrient_json["carbohydrate"],
                "sugar": None,
                "protein": nutrient_json["protein"],
                "salt": None,
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_tags(self, recipe_json, recipe):
        for tag_json in recipe_json["tags"]:
            cuisine_tg = None
            if tag_json["type"] == "cuisine":
                cuisine_tg, created = TagGroup.objects.get_or_create(name="Cuisine")
            tag = Tag.objects.update_or_create(
                helloFreshId=tag_json["id"],
                defaults={
                    "name": tag_json["title"],
                    "type": tag_json["type"],
                    "tagGroup": cuisine_tg
                }
            )
            if tag is None:
                continue
            tag = tag[0]
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
        for i, step_json in enumerate(recipe_json["steps"]):
            if ("image" in step_json) and step_json["image"]["url"] is not None:
                image_url = step_json["image"]["url"]
            else:
                image_url = None
            step = WorkSteps.objects.update_or_create(
                id=recipe.helloFreshId + str(i),
                defaults={
                    "relatedRecipe": recipe,
                    "index": i,
                    "description": step_json["text"],
                    "HelloFreshImageUrl": image_url
                }
            )[0]
            if (not (step.image and step.image.file)) and global_preferences[
                'scraper__Download_Process_Step_Images'] and image_url is not None:
                try:
                    step.image.save(str(uuid.uuid4()) + ".png", self.get_image(image_url))
                except:
                    print(f"Could not save process-step-image for step {step}")

    def scrape(self, index):
        response = requests.request("GET",
                                    f"https://web-bff.services.kitchenstories.io/api/recipes/?page={index}&page_size={self.PAGE_SIZE}&language={self.country}")
        items = response.json()["data"]
        self.config.set_ks_max_page(response.json()["meta"]["pagination"]["pages"])
        for recipeJson in items:
            try:
                temp = self.create_recipe(recipeJson)
                if temp is None:
                    logging.warning(f"Skipping recipe with id {recipeJson['id']} (index: {index})")
                    continue
                recipe, created = temp
                self.create_ingredients(recipeJson, recipe)
                self.create_utensil(recipeJson, recipe)
                self.create_nutrients(recipeJson, recipe)
                self.create_tags(recipeJson, recipe)
                self.create_work_steps(recipeJson, recipe)
                self.last_error = False
                if created:
                    logging.info(f"Successfully created recipe with id {recipeJson['id']} (index: {index})")
                else:
                    logging.debug(f"Successfully updated recipe with id {recipeJson['id']} (index: {index})")
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
