import os
import sqlite3
import threading
import uuid
from datetime import timedelta, datetime

import pytz
from dynamic_preferences.registries import global_preferences_registry

from src.HelloMeals.settings import BASE_DIR
from .common import get_image
from ...models import *

global_preferences = global_preferences_registry.manager()


class Scraper:
    def run(self):
        tz = pytz.timezone("Europe/Berlin")
        path = os.path.join(BASE_DIR, "data", "recipes.db")
        print(f"Looking for yazio db at path: {path}")
        if not os.path.exists(path) or not global_preferences['general__General_Yazio_Scrape']:
            return
        print("starting to scrape yazio recipes from database")
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        recipes = cur.execute("SELECT * FROM recipe").fetchall()
        for recipe in recipes:
            # Create Recipe
            image_url = recipe[7]
            r = Recipe.objects.update_or_create(
                helloFreshId="y" + recipe[1],
                defaults={
                    "name": recipe[2],
                    "source": 6,
                    "description": recipe[3],
                    "HelloFreshImageUrl": image_url,
                    "servings": recipe[8],
                    "createdAt": recipe[9] + " 00:00:00+02:00",
                    "updatedAt": datetime.fromtimestamp(recipe[13], tz),
                    "prepTime": timedelta(minutes=recipe[10]),
                    "totalTime": timedelta(minutes=recipe[10]),
                    "averageRating": 5,
                    "ratingCount": round((2500 - recipe[11]) ** 0.8),
                    "difficulty": 1 if recipe[4] == "Easy" else 2 if recipe[4] == "Normal" else 3 if recipe[
                                                                                                         4] == "Hard" else 1
                })[0]
            if (not (r.image and r.image.file)) and global_preferences[
                'scraper__Download_Recipe_Images']:
                image = get_image(image_url)
                if image is not None:
                    r.image.save(str(uuid.uuid4()) + ".png", image)
            # Create work steps
            steps = cur.execute(f"SELECT * FROM recipeInstruction where recipeId = '{recipe[0]}'").fetchall()
            for i, step in enumerate(steps):
                s = WorkSteps.objects.update_or_create(
                    id=r.helloFreshId + str(i),
                    defaults={
                        "relatedRecipe": r,
                        "index": i,
                        "description": step[1],
                    }
                )[0]
                s.save()

            # Create Nutrients
            nutrients = cur.execute(f"SELECT * FROM recipeNutrient where recipeId = '{recipe[0]}'").fetchall()
            energy = [n[2] for n in nutrients if n[1] == 'energy.energy']
            fat = [n[2] for n in nutrients if n[1] == 'nutrient.fat']
            protein = [n[2] for n in nutrients if n[1] == 'nutrient.protein']
            carbs = [n[2] for n in nutrients if n[1] == 'nutrient.carb']
            salt = [n[2] for n in nutrients if n[1] == 'nutrient.salt']
            sugar = [n[2] for n in nutrients if n[1] == 'nutrient.sugar']
            n = Nutrients.objects.update_or_create(
                id=r.helloFreshId + "n",
                defaults={
                    "recipe": r,
                    "energyKcal": energy[0] if len(energy) > 0 else None,
                    "fat": fat[0] if len(fat) > 0 else None,
                    "protein": protein[0] if len(protein) > 0 else None,
                    "carbs": carbs[0] if len(carbs) > 0 else None,
                    "salt": salt[0] if len(salt) > 0 else None,
                    "sugar": sugar[0] if len(sugar) > 0 else None,
                }
            )[0]
            r.nutrients = n

            # Create Ingredients
            ingredients = cur.execute(f"SELECT * FROM recipeServing where recipeId = '{recipe[0]}'").fetchall()
            for i, ingredient in enumerate(ingredients):
                sg = IngredientGroup.objects.update_or_create(id=r.helloFreshId + "ig", defaults={"name": None})[0]
                s = Ingredient.objects.update_or_create(
                    helloFreshId=r.helloFreshId + str(ingredient[0]),
                    defaults={
                        "name": ingredient[2],
                    }
                )[0]
                unit = ingredient[8] if ingredient[8] else "Esslöffel" if ingredient[
                                                                              4] == "Tablespoon" else "Teelöffel" if \
                    ingredient[4] == "Teaspoon" else "ml" if ingredient[7] == "1" and not ingredient[6] else "g" if not \
                    ingredient[6] else None
                recipe_ingredient = RecipeIngredient.objects.update_or_create(
                    id=s.helloFreshId + sg.id,
                    defaults={
                        "ingredient_group": sg,
                        "ingredient": s,
                        "amount": ingredient[6] if ingredient[6] else ingredient[3],
                        "unit": unit,
                    }
                )[0]
                recipe_ingredient.save()
                s.save()
                sg.save()
                r.ingredient_groups.add(sg)

            # Create tags
            tags = cur.execute(f"SELECT * FROM recipeTag where recipeId = '{recipe[0]}'").fetchall()
            for i, tag in enumerate(tags):
                if tag[1] == "Lunch" or tag[1] == "Dinner":
                    r.recipeType = 0
                elif tag[1] == "Breakfast":
                    r.recipeType = 1
                elif tag[1] == "Dessert":
                    r.recipeType = 2
                elif tag[1] == "Baking":
                    r.recipeType = 3
                elif tag[1] == "Smoothie" or tag[1] == "Shake":
                    r.recipeType = 4
                t = Tag.objects.update_or_create(
                    helloFreshId="y" + tag[1],
                    defaults={
                        "name": tag[1]
                    }
                )[0]
                recipe_tag = RecipeTag.objects.update_or_create(
                    id=r.helloFreshId + t.helloFreshId,
                    defaults={
                        "recipe": r,
                        "tag": t,
                    }
                )[0]
                recipe_tag.save()
                t.save()

            r.save()
        print("Yazio Scraping finished")
        global_preferences['general__General_Yazio_Scrape'] = False


threading.Thread(target=Scraper().run, args=(), daemon=True).start()
