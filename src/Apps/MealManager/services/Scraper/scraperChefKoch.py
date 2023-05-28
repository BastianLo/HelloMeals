import logging
import os
import re
import threading
from datetime import timedelta

import requests

from .scrapeConfig import scrapeConfig
from ...models import *


def is_valid_iso_duration(duration_str):
    pattern = r'^P(?:\d+Y)?(?:\d+M)?(?:\d+W)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$'
    return re.match(pattern, duration_str) is not None


# TODO: for scraper functionality:
# eg: functionality to redownload images (to improve quality)
# Possibly increase recipe quality compared to other images
class Scraper:
    def __init__(self):
        self.exception = None
        self.last_error = False
        self.limit = 2
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = scrapeConfig()
        self.active = False
        self.country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"
        self.download_images = os.getenv('DOWNLOAD_IMAGES') if os.getenv('DOWNLOAD_IMAGES') else True

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
                self.config.set_hf_start_index(self.config.hf_start_index + self.limit)
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

    def get_image(self, url):
        if url is None:
            return None
        try:
            img_tmp = NamedTemporaryFile(delete=True)
            with urlopen(url) as uo:
                assert uo.status == 200
                img_tmp.write(uo.read())
                img_tmp.flush()
            img = File(img_tmp)
            return img
        except:
            return None

    def create_recipe(self, recipe_json):
        if recipe_json["previewImageUrlTemplate"] is None:
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
        if (not (recipe[0].image and recipe[0].image.file)) and self.download_images:
            image = self.get_image(image_url)
            if image is not None:
                recipe[0].image.save(str(uuid.uuid4()) + ".png", image)
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        for group_json in recipe_json["ingredientGroups"]:
            for ingredient_json in group_json["ingredients"]:
                ingredient = Ingredient.objects.update_or_create(
                    helloFreshId=ingredient_json["id"],
                    defaults={
                        "name": ingredient_json["name"],
                    }
                )[0]
                # Create RecipeIngredient
                ingredient_id = ingredient_json["id"]
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=ingredient_id + recipe.helloFreshId,
                    defaults={
                        "recipe": recipe,
                        "ingredient": ingredient,
                        "amount": ingredient_json["amount"],
                        "unit": ingredient_json["unit"],
                    }
                )[0]

    def create_nutrients(self, recipe_json, recipe):
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


    def create_cuisine(self, recipe_json, recipe):
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


    def create_tags(self, recipe_json, recipe):
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


    def create_categories(self, recipe_json, recipe):
        if recipe_json["category"] is None:
            return None
        category_json = recipe_json["category"]
        category = Category.objects.update_or_create(
            helloFreshId=category_json["id"],
            defaults={
                "name": category_json["name"],
                "type": category_json["type"],
            }
        )[0]
        recipe.category = category


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
            if (not (step.image and step.image.file)) and (len(step_json["images"]) > 0) and self.download_images:
                try:
                    step.image.save(str(uuid.uuid4()) + ".png", self.get_image(image_url))
                except:
                    print(f"Could not save process-step-image for step {step}")


    def scrape(self, index):
        chefkoch_url = f"https://api.chefkoch.de/v2/search-gateway/recipes?tags=21&minimumRating=4.2&limit={self.limit}&offset={index}"
        response = requests.request("GET", chefkoch_url)
        items = response.json()["results"]
        self.config.set_hf_max_recipes(response.json()["count"])
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
                print("finish")
                exit()
                self.create_cuisine(new_recipe_json, recipe)
                self.create_tags(new_recipe_json, recipe)
                self.create_categories(new_recipe_json, recipe)
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
