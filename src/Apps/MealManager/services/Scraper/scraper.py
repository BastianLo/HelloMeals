import json
import os
import threading

import requests
from HelloMeals import settings
from ...models import *
from isodate import parse_duration
from django.core.files.base import File


class ScrapeConfig:
    def __init__(self):
        self.path = str(settings.BASE_DIR) + "/data/config/scraper.json"
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config_data = json.load(f)
        else:
            self.config_data = {}
        self.start_index = self.config_data["start_index"] if "start_index" in self.config_data else 0
        self.max_recipes = self.config_data["max_recipes"] if "max_recipes" in self.config_data else 1000000

    def set_start_index(self, start_index):
        self.start_index = start_index
        self.save_file()

    def set_max_recipes(self, max_recipes):
        self.max_recipes = max_recipes
        self.save_file()

    def save_file(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.mkdir(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            json.dump({
                "start_index": self.start_index,
                "max_recipes": self.max_recipes,
            }, f)


class Scraper:
    def __init__(self):
        self.exception = None
        self.work_thread = threading.Thread(target=self.work, args=(), daemon=True)
        self.config = ScrapeConfig()
        self.active = False
        self.country = os.getenv('COUNTRY') if os.getenv('COUNTRY') else "DE"
        self.HELLO_FRESH_URL = f"https://www.hellofresh.de/gw/api/recipes?country={self.country}&order=-favorites&take=1&skip="
        self.bearer_token = None
        self.download_images = os.getenv('DOWNLOAD_IMAGES') if os.getenv('DOWNLOAD_IMAGES') else True

    def get_status(self):
        return {
            "max_recipes": self.config.max_recipes,
            "start_index": self.config.start_index,
            "running": self.is_running(),
            "exception": self.exception
        }

    def work(self):
        try:
            while self.active and self.config.start_index < self.config.max_recipes:
                self.scrape(self.config.start_index)
                self.config.set_start_index(self.config.start_index + 1)
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
        image_url = "https://img.hellofresh.com/q_40,w_720,f_auto,c_limit,fl_lossy/hellofresh_s3" + recipe_json[
                    "imagePath"]
        if recipe_json["yields"] is None or len(recipe_json["yields"]) == 0:
            return None
        recipe = Recipe.objects.update_or_create(
            helloFreshId=recipe_json["id"],
            defaults={
                "name": recipe_json["name"],
                "headline": recipe_json["headline"],
                "description": recipe_json["description"],
                "cardLink": recipe_json["cardLink"],
                "websiteLink": recipe_json["canonicalLink"],
                "prepTime": parse_duration(recipe_json["prepTime"]) if recipe_json["prepTime"] and recipe_json["prepTime"] != "0" else None,
                "totalTime": parse_duration(recipe_json["totalTime"]) if recipe_json["totalTime"] and recipe_json["totalTime"] != "0" else None,
                "difficulty": recipe_json["difficulty"],
                "createdAt": recipe_json["createdAt"],
                "updatedAt": recipe_json["updatedAt"],
                "favoritesCount": recipe_json["favoritesCount"],
                "averageRating": recipe_json["averageRating"],
                "ratingCount": recipe_json["ratingsCount"],
                "servings": recipe_json["yields"][-1]["yields"],
                "HelloFreshImageUrl": image_url
            }
        )[0]
        if (not (recipe.image and recipe.image.file)) and self.download_images:
            image = self.get_image(image_url)
            if image is not None:
                recipe.image.save(str(uuid.uuid4()) + ".png", image)
        return recipe

    def create_ingredients(self, recipe_json, recipe):
        yields = recipe_json["yields"][-1]["ingredients"]
        for ingredient_json in recipe_json["ingredients"]:
            if "imagePath" in ingredient_json and ingredient_json["imagePath"] is not None:
                image_url = "https://img.hellofresh.com/q_40,w_480,f_auto,c_limit,fl_lossy/hellofresh_s3" + ingredient_json[
                            "imagePath"]
            else:
                image_url = None
            ingredient = Ingredient.objects.update_or_create(
                helloFreshId=ingredient_json["id"],
                defaults={
                    "name": ingredient_json["name"],
                    "HelloFreshImageUrl": image_url
                }
            )[0]
            if (not (ingredient.image and ingredient.image.file)) and self.download_images:
                image = self.get_image(image_url)
                if image is not None:
                    ingredient.image.save(str(uuid.uuid4()) + ".png", image)
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
                "energyKj": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530d"]), 0),
                "energyKcal": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305304"]), 0),
                "fat": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305307"]), 0),
                "fatSaturated": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305308"]), 0),
                "carbs": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305305"]), 0),
                "sugar": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305306"]), 0),
                "protein": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b305309"]), 0),
                "salt": next(iter([n["amount"] for n in nutrient_json if n["type"] == "57b42a48b7e8697d4b30530b"]), 0),
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

    def create_work_steps(self, recipe_json, recipe):
        for step_json in recipe_json["steps"]:
            if (len(step_json["images"]) > 0) and step_json["images"][0]["link"] is not None:
                image_url = "https://img.hellofresh.com/q_40,w_480,f_auto,c_limit,fl_lossy/hellofresh_s3" + step_json["images"][0]["path"]
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
        headers = {
            'authorization': f'Bearer {self.bearer()}',
        }
        response = requests.request("GET", self.HELLO_FRESH_URL + str(index), headers=headers)
        items = response.json()["items"]
        self.config.set_max_recipes(response.json()["total"])
        for recipeJson in items:
            recipe = self.create_recipe(recipeJson)
            if recipe is None:
                continue
            self.create_ingredients(recipeJson, recipe)
            self.create_utensil(recipeJson, recipe)
            self.create_nutrients(recipeJson, recipe)
            self.create_cuisine(recipeJson, recipe)
            self.create_tags(recipeJson, recipe)
            self.create_work_steps(recipeJson, recipe)


s = Scraper()


def get_scraper():
    global s
    return s
