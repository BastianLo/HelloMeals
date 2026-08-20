from django.test import TestCase
from dynamic_preferences.registries import global_preferences_registry

from Apps.MealManager.models import Recipe
from Apps.MealManager.services.Scraper.scraper import Scraper


def _minimal_recipe_json(**overrides):
    base = {
        "id": "hf-test-1",
        "name": "Test Recipe",
        "imagePath": "/some/image.jpg",
        "yields": [{"yields": 4, "ingredients": []}],
        "clonedFrom": None,
        "videoLink": None,
        "isAddon": False,
        "active": True,
        "headline": "Headline",
        "description": "Description",
        "cardLink": None,
        "canonicalLink": "https://example.com/recipe",
        "prepTime": None,
        "totalTime": None,
        "difficulty": 1,
        "createdAt": None,
        "updatedAt": None,
        "favoritesCount": 0,
        "averageRating": 0,
        "ratingsCount": 0,
    }
    base.update(overrides)
    return base


class HelloFreshCreateRecipeTests(TestCase):
    """Regression test for a live-scraping crash: HelloFresh's API stopped returning the
    "highlighted", "isDinnerToLunch", "isExcludedFromIndex", "isPremium" and "author" fields,
    and create_recipe used to index them directly instead of via .get(...)."""

    def setUp(self):
        # avoid a real network call to download the (fake) recipe image in these tests
        global_preferences_registry.manager()['scraper__Download_Recipe_Images'] = False

    def test_missing_optional_fields_do_not_crash(self):
        recipe_json = _minimal_recipe_json()
        for missing_field in ("highlighted", "isDinnerToLunch", "isExcludedFromIndex", "isPremium", "author"):
            recipe_json.pop(missing_field, None)

        scraper = Scraper()
        result = scraper.create_recipe(recipe_json)

        self.assertIsNotNone(result)
        recipe, _created = result
        self.assertEqual(recipe.name, "Test Recipe")
        self.assertIsNone(recipe.highlighted)
        self.assertIsNone(recipe.isDinnerToLunch)
        self.assertIsNone(recipe.isExcludedFromIndex)
        self.assertIsNone(recipe.isPremium)
        self.assertIsNone(recipe.author)

    def test_present_optional_fields_are_still_used(self):
        recipe_json = _minimal_recipe_json(author="Chef Test", isPremium=True)

        scraper = Scraper()
        recipe, _created = scraper.create_recipe(recipe_json)

        self.assertEqual(recipe.author, "Chef Test")
        self.assertTrue(recipe.isPremium)
