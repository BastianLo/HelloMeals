import logging
import os
import threading
import uuid

import requests
from dynamic_preferences.registries import global_preferences_registry
from isodate import parse_duration

from .common import get_image, is_valid_iso_duration
from .scrapeConfig import scrapeConfig
from ...models import *

global_preferences = global_preferences_registry.manager()


# TagMerge.objects.create(source="57ebbc17b7e8697d4b3053ac", target="57ebbc17b7e8697d4b3053b5")

# TODO: for scraper functionality:
# eg: functionality to redownload images (to improve quality)
# Possibly increase recipe quality compared to other images
class Scraper:
    def __init__(self):
        self.exception = None
        self.last_error = False
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = scrapeConfig()
        self.active = False
        self.country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"
        self.HELLO_FRESH_URL = f"https://www.hellofresh.de/gw/api/recipes?country={self.country}&order=-date&take=1&skip="
        self.bearer_token = None

    def get_status(self):
        return {
            "max_recipes": self.config.hf_max_recipes,
            "start_index": self.config.hf_start_index,
            "running": self.is_running(),
            "exception": self.exception
        }

    def work(self):
        try:
            while self.active and self.config.hf_start_index < self.config.hf_max_recipes:
                self.scrape(self.config.hf_start_index)
                self.config.set_hf_start_index(self.config.hf_start_index + 1)
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
        self.config.set_hf_start_index(index)

    def restart(self):
        self.stop()
        self.config.set_hf_start_index(0)
        self.start()

    def is_running(self):
        return self.work_thread.is_alive()

    def bearer(self):
        if self.bearer_token is not None:
            return self.bearer_token
        url = "https://www.hellofresh.de"
        html = requests.get(url)
        token = html.text[html.text.index("access_token"):]
        token = token[token.index(":") + 2:]
        token = token[:token.index('"')]
        bearer_token = token
        return bearer_token

    def create_recipe(self, recipe_json):
        if recipe_json["imagePath"] is None:
            return None
        image_url = "https://img.hellofresh.com/q_40,w_720,f_auto,c_limit,fl_lossy/hellofresh_s3" + recipe_json[
            "imagePath"]
        if recipe_json["yields"] is None or len(recipe_json["yields"]) == 0:
            return None
        recipe = Recipe.objects.update_or_create(
            helloFreshId=recipe_json["id"],
            defaults={
                "name": recipe_json["name"],
                "source": 1,
                "clonedFrom": recipe_json["clonedFrom"],
                "videoLink": recipe_json["videoLink"],
                "highlighted": recipe_json["highlighted"],
                "isAddon": recipe_json["isAddon"],
                "isDinnerToLunch": recipe_json["isDinnerToLunch"],
                "isExcludedFromIndex": recipe_json["isExcludedFromIndex"],
                "isPremium": recipe_json["isPremium"],
                "author": recipe_json["author"],
                "helloFreshActive": recipe_json["active"],
                "headline": recipe_json["headline"],
                "description": recipe_json["description"],
                "cardLink": recipe_json["cardLink"],
                "websiteLink": recipe_json["canonicalLink"],
                "prepTime": parse_duration(recipe_json["prepTime"]) if recipe_json[
                                                                           "prepTime"] and is_valid_iso_duration(
                    recipe_json["prepTime"]) and recipe_json["prepTime"] != "0" else None,
                "totalTime": parse_duration(recipe_json["totalTime"]) if recipe_json[
                                                                             "totalTime"] and is_valid_iso_duration(
                    recipe_json["totalTime"]) and recipe_json["totalTime"] != "0" else None,
                "difficulty": recipe_json["difficulty"],
                "createdAt": recipe_json["createdAt"],
                "updatedAt": recipe_json["updatedAt"],
                "favoritesCount": recipe_json["favoritesCount"],
                "averageRating": recipe_json["averageRating"],
                "ratingCount": recipe_json["ratingsCount"],
                "servings": recipe_json["yields"][-1]["yields"] if len(recipe_json["yields"]) > 0 else None,
                "HelloFreshImageUrl": image_url
            }
        )
        if (not (recipe[0].image and recipe[0].image.file)) and global_preferences['scraper__Download_Recipe_Images']:
            image = get_image(image_url)
            if image is not None:
                recipe[0].image.save(str(uuid.uuid4()) + ".png", image)
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        ingredient_group = IngredientGroup.objects.update_or_create(
            id=recipe.helloFreshId + "0",
            defaults={
                "name": None,
            }
        )[0]
        recipe.ingredient_groups.add(ingredient_group)
        recipe.save()
        yields = recipe_json["yields"][-1]["ingredients"]
        for ingredient_json in recipe_json["ingredients"]:
            if "imagePath" in ingredient_json and ingredient_json["imagePath"] is not None:
                image_url = "https://img.hellofresh.com/q_40,w_480,f_auto,c_limit,fl_lossy/hellofresh_s3" + \
                            ingredient_json[
                                "imagePath"]
            else:
                image_url = None
            ingredient = Ingredient.objects.update_or_create(
                helloFreshId=ingredient_json["id"],
                defaults={
                    "name": ingredient_json["name"].replace("*", ""),
                    "HelloFreshImageUrl": image_url
                }
            )[0]
            if (not (ingredient.image and ingredient.image.file)) and global_preferences[
                'scraper__Download_Ingredient_Images']:
                image = get_image(image_url)
                if image is not None:
                    ingredient.image.save(str(uuid.uuid4()) + ".png", image)
            # Create RecipeIngredient
            ingredient_id = ingredient_json["id"]
            ingredient_yield = [y for y in yields if y["id"] == ingredient_id][0]
            recipe_ingredient = RecipeIngredient.objects.update_or_create(
                id=ingredient_id + ingredient_group.id,
                defaults={
                    "ingredient_group": ingredient_group,
                    "ingredient": ingredient,
                    "amount": ingredient_yield["amount"],
                    "unit": ingredient_yield["unit"],
                }
            )[0]

    def create_utensil(self, recipe_json, recipe):
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

    def create_nutrients(self, recipe_json, recipe):
        nutrient_json = recipe_json["nutrition"]
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKj": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530d"]),
                                 0),
                "energyKcal": next(
                    iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305304"]), 0),
                "fat": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305307"]), 0),
                "fatSaturated": next(
                    iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305308"]), 0),
                "carbs": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305305"]), 0),
                "sugar": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305306"]), 0),
                "protein": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305309"]),
                                0),
                "salt": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530b"]), 0),
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_cuisine(self, recipe_json, recipe):
        cuisine_tg, created = TagGroup.objects.get_or_create(name="Cuisine")
        for cuisine_json in recipe_json["cuisines"]:
            cuisine = Tag.objects.update_or_create(
                helloFreshId=cuisine_json["id"],
                defaults={
                    "name": cuisine_json["name"],
                    "type": cuisine_json["type"],
                    "tagGroup": cuisine_tg
                }
            )
            if cuisine is None:
                continue
            cuisine = cuisine[0]
            recipe_cuisine = RecipeTag.objects.update_or_create(
                id=recipe.helloFreshId + cuisine.helloFreshId,
                defaults={
                    "recipe": recipe,
                    "tag": cuisine,
                }
            )

    def create_tags(self, recipe_json, recipe):
        for tag_json in recipe_json["tags"]:
            tag = Tag.objects.update_or_create(
                helloFreshId=tag_json["id"],
                defaults={
                    "name": tag_json["name"],
                    "type": tag_json["type"],
                }
            )
            if tag is None:
                continue
            tag = tag[0]
            temp = RecipeTag.objects.filter(recipe=recipe, tag=tag)
            if len(temp) == 0:
                recipe_tag = RecipeTag.objects.update_or_create(
                    id=recipe.helloFreshId + tag.helloFreshId,
                    defaults={
                        "recipe": recipe,
                        "tag": tag,
                    }
                )

    def create_work_steps(self, recipe_json, recipe):
        for step_json in recipe_json["steps"]:
            if (len(step_json["images"]) > 0) and step_json["images"][0]["link"] is not None:
                image_url = "https://img.hellofresh.com/q_40,w_480,f_auto,c_limit,fl_lossy/hellofresh_s3" + \
                            step_json["images"][0]["path"]
            else:
                image_url = None
            step = WorkSteps.objects.update_or_create(
                id=recipe.helloFreshId + str(step_json["index"]),
                defaults={
                    "relatedRecipe": recipe,
                    "index": step_json["index"],
                    "description": step_json["instructions"],
                    "HelloFreshImageUrl": image_url
                }
            )[0]
            if (not (step.image and step.image.file)) and (len(step_json["images"]) > 0) and global_preferences[
                'scraper__Download_Process_Step_Images']:
                try:
                    step.image.save(str(uuid.uuid4()) + ".png", get_image(image_url))
                except:
                    print(f"Could not save process-step-image for step {step}")

    def scrape(self, index):
        if index % 500 == 0:
            self.bearer_token = None
        headers = {
            'authorization': f'Bearer {self.bearer()}',
        }
        response = requests.request("GET", self.HELLO_FRESH_URL + str(index), headers=headers)
        items = response.json()["items"]
        self.config.set_hf_max_recipes(response.json()["total"])
        for recipeJson in items:
            try:
                recipe_id = recipeJson["id"]
                url = f"https://www.hellofresh.de/gw/recipes/recipes/{recipe_id}"
                new_recipe_json = requests.get(url, headers=headers).json()
                temp = self.create_recipe(new_recipe_json)
                if temp is None:
                    logging.warning(f"Skipping recipe with id {recipe_id} (index: {index})")
                    continue
                recipe, created = temp
                self.create_ingredients(new_recipe_json, recipe)
                self.create_utensil(new_recipe_json, recipe)
                self.create_nutrients(new_recipe_json, recipe)
                self.create_cuisine(new_recipe_json, recipe)
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
