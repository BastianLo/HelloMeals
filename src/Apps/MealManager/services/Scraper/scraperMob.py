import json
import logging
import re

import requests
from dynamic_preferences.registries import global_preferences_registry
from isodate import parse_duration

from ...models import *
from .baseScraper import BaseScraper
from .common import is_valid_iso_duration, maybe_save_image

global_preferences = global_preferences_registry.manager()

SITEMAP_URL = "https://www.mob.co.uk/sitemaps-1-section-recipes-1-sitemap-p{page}.xml"
SITEMAP_PAGES = 9

# Mob concatenates the unit directly onto the amount with no space (e.g. "160g Tahini",
# "2tbsp Gochujang"), while amounts with no unit are followed by a space straight into the
# name (e.g. "6 Garlic Clove", "1 Egg"). Whether a space follows the number is therefore what
# distinguishes a unit from the start of the ingredient name, not the word itself.
AMOUNT_UNIT_RE = re.compile(r"^\s*([\d.,/]+)([a-zA-Zµ]+)\s+(.+)$")
AMOUNT_ONLY_RE = re.compile(r"^\s*([\d.,/]+)\s+(.+)$")


def parse_amount(amount_str):
    amount_str = amount_str.replace(",", ".")
    try:
        if "/" in amount_str:
            numerator, denominator = amount_str.split("/")
            return float(numerator) / float(denominator)
        return float(amount_str)
    except (ValueError, ZeroDivisionError):
        return None


def parse_ingredient(ingredient_str):
    ingredient_str = ingredient_str.strip()
    match = AMOUNT_UNIT_RE.match(ingredient_str)
    if match:
        return parse_amount(match.group(1)), match.group(2), match.group(3).strip()
    match = AMOUNT_ONLY_RE.match(ingredient_str)
    if match:
        return parse_amount(match.group(1)), None, match.group(2).strip()
    return None, None, ingredient_str


def extract_number(value):
    if value is None:
        return None
    match = re.search(r"[\d.,]+", str(value))
    if not match:
        return None
    try:
        return int(float(match.group(0).replace(",", ".")))
    except ValueError:
        return None


def extract_image(image_field):
    if image_field is None:
        return None
    if isinstance(image_field, str):
        return image_field
    if isinstance(image_field, list) and len(image_field) > 0:
        return extract_image(image_field[0])
    if isinstance(image_field, dict):
        return image_field.get("url")
    return None


def extract_name(entity):
    if entity is None:
        return None
    if isinstance(entity, str):
        return entity
    if isinstance(entity, list) and len(entity) > 0:
        return extract_name(entity[0])
    if isinstance(entity, dict):
        return entity.get("name")
    return None


def flatten_instructions(instructions):
    steps = []
    if instructions is None:
        return steps
    if isinstance(instructions, str):
        return [s.strip() for s in instructions.split("\n") if s.strip()]
    for item in instructions:
        if isinstance(item, str):
            steps.append(item.strip())
        elif isinstance(item, dict):
            if item.get("@type") == "HowToSection" and "itemListElement" in item:
                steps.extend(flatten_instructions(item["itemListElement"]))
            elif "text" in item:
                steps.append(item["text"].strip())
    return steps


class Scraper(BaseScraper):
    config_key = "mob"

    def __init__(self):
        super().__init__()
        self.urls = []

    def fetch_urls(self):
        urls = []
        for page in range(1, SITEMAP_PAGES + 1):
            response = requests.get(SITEMAP_URL.format(page=page), headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                continue
            urls += re.findall(r"<loc>(.*?)</loc>", response.text)
        self.urls = urls
        self.set_max(len(urls))
        return urls

    def work(self):
        urls = self.fetch_urls()
        while self.active and self.get_index() < len(urls):
            self.scrape(urls[self.get_index()], self.get_index())
            self.set_index(self.get_index() + 1)

    def fetch_recipe_json(self, url):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.DOTALL)
        for block in blocks:
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            if data.get("@type") == "Recipe":
                return data
        return None

    def guess_recipe_type(self, recipe_json):
        categories = (recipe_json.get("recipeCategory") or "").lower()
        if "dessert" in categories:
            return Recipe.RecipeTypes.dessert
        if "breakfast" in categories or "brunch" in categories:
            return Recipe.RecipeTypes.breakfast
        if "bak" in categories or "cake" in categories:
            return Recipe.RecipeTypes.baking
        if "cocktail" in categories or "drink" in categories or "smoothie" in categories:
            return Recipe.RecipeTypes.drink
        return Recipe.RecipeTypes.main

    def create_recipe(self, recipe_json, url):
        if recipe_json.get("name") is None:
            return None
        image_url = extract_image(recipe_json.get("image"))
        rating = recipe_json.get("aggregateRating") or {}
        recipe = Recipe.objects.update_or_create(
            helloFreshId="mob" + str(recipe_json.get("identifier") or url),
            defaults={
                "name": recipe_json["name"],
                "source": Recipe.Source.mob,
                "recipeType": self.guess_recipe_type(recipe_json),
                "author": extract_name(recipe_json.get("author")),
                "description": recipe_json.get("description"),
                "websiteLink": recipe_json.get("url") or url,
                "prepTime": parse_duration(recipe_json["prepTime"]) if recipe_json.get(
                    "prepTime") and is_valid_iso_duration(recipe_json["prepTime"]) else None,
                "totalTime": parse_duration(recipe_json["totalTime"]) if recipe_json.get(
                    "totalTime") and is_valid_iso_duration(recipe_json["totalTime"]) else None,
                "averageRating": rating.get("ratingValue"),
                "ratingCount": rating.get("ratingCount"),
                "servings": extract_number(recipe_json.get("recipeYield")),
                "HelloFreshImageUrl": image_url
            }
        )
        maybe_save_image(recipe[0], image_url, 'scraper__Download_Recipe_Images')
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
        for i, ingredient_str in enumerate(recipe_json.get("recipeIngredient") or []):
            amount, unit, name = parse_ingredient(ingredient_str)
            if not name:
                continue
            ingredient = Ingredient.objects.update_or_create(
                helloFreshId=recipe.helloFreshId + "i" + str(i),
                defaults={
                    "name": name,
                }
            )[0]
            recipe_ingredient = RecipeIngredient.objects.update_or_create(
                id=ingredient.helloFreshId + ingredient_group.id,
                defaults={
                    "ingredient_group": ingredient_group,
                    "ingredient": ingredient,
                    "amount": amount,
                    "unit": unit,
                }
            )[0]

    def create_nutrients(self, recipe_json, recipe):
        nutrient_json = recipe_json.get("nutrition")
        if not nutrient_json:
            return
        nutrient = Nutrients.objects.update_or_create(
            id=recipe.helloFreshId + "nutrients",
            defaults={
                "energyKcal": extract_number(nutrient_json.get("calories")),
                "fat": extract_number(nutrient_json.get("fatContent")),
                "fatSaturated": extract_number(nutrient_json.get("saturatedFatContent")),
                "carbs": extract_number(nutrient_json.get("carbohydrateContent")),
                "sugar": extract_number(nutrient_json.get("sugarContent")),
                "protein": extract_number(nutrient_json.get("proteinContent")),
            }
        )[0]
        recipe.nutrients = nutrient
        recipe.save()

    def create_tags(self, recipe_json, recipe):
        category_tg, created = TagGroup.objects.get_or_create(name="Category")
        categories = [c.strip() for c in (recipe_json.get("recipeCategory") or "").split(",") if c.strip()]
        for category in categories:
            tag = Tag.objects.update_or_create(
                helloFreshId="mob" + category.lower().replace(" ", "_"),
                defaults={
                    "name": category,
                    "type": "category",
                    "tagGroup": category_tg
                }
            )
            if tag is None:
                continue
            tag = tag[0]
            try:
                RecipeTag.objects.update_or_create(
                    id=recipe.helloFreshId + tag.helloFreshId,
                    defaults={
                        "recipe": recipe,
                        "tag": tag,
                    }
                )
            except Exception:
                continue

        cuisine = (recipe_json.get("recipeCuisine") or "").strip()
        if cuisine:
            cuisine_tg, created = TagGroup.objects.get_or_create(name="Cuisine")
            tag = Tag.objects.update_or_create(
                helloFreshId="mob" + cuisine.lower().replace(" ", "_"),
                defaults={
                    "name": cuisine,
                    "type": "cuisine",
                    "tagGroup": cuisine_tg
                }
            )
            if tag is not None:
                tag = tag[0]
                try:
                    RecipeTag.objects.update_or_create(
                        id=recipe.helloFreshId + tag.helloFreshId,
                        defaults={
                            "recipe": recipe,
                            "tag": tag,
                        }
                    )
                except Exception:
                    pass

    def create_work_steps(self, recipe_json, recipe):
        steps = flatten_instructions(recipe_json.get("recipeInstructions"))
        for i, step_text in enumerate(steps):
            WorkSteps.objects.update_or_create(
                id=recipe.helloFreshId + str(i),
                defaults={
                    "relatedRecipe": recipe,
                    "index": i,
                    "description": step_text,
                }
            )

    def scrape(self, url, index):
        try:
            recipe_json = self.fetch_recipe_json(url)
            if recipe_json is None:
                logging.warning(f"Skipping url {url} (index: {index}) - no Recipe JSON-LD found")
                return
            temp = self.create_recipe(recipe_json, url)
            if temp is None:
                logging.warning(f"Skipping recipe at {url} (index: {index})")
                return
            recipe, created = temp
            self.create_ingredients(recipe_json, recipe)
            self.create_nutrients(recipe_json, recipe)
            self.create_tags(recipe_json, recipe)
            self.create_work_steps(recipe_json, recipe)
            self.last_error = False
            if created:
                logging.info(f"Successfully created recipe with id {recipe.helloFreshId} (index: {index})")
            else:
                logging.debug(f"Successfully updated recipe with id {recipe.helloFreshId} (index: {index})")
        except Exception as e:
            self.handle_scrape_error(e, f"Recipe at '{url}' (index: {index})")


s = Scraper()


def get_scraper():
    global s
    return s
