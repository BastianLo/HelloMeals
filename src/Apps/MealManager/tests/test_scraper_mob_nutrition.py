from django.test import TestCase

from Apps.MealManager.models import Recipe
from Apps.MealManager.services.Scraper.scraperMob import Scraper


class CreateNutrientsTests(TestCase):
    """Regression coverage for the fix that made Mob nutrition actually get saved - see
    ExtractPageNutritionTests for why the data has to come from __NEXT_DATA__ in the first
    place instead of the schema.org JSON-LD."""

    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="mob1", name="Test Recipe")
        self.scraper = Scraper()

    def test_saves_real_values_and_converts_sodium_to_salt(self):
        self.scraper.create_nutrients(self.recipe, {
            "calories": 834, "fat": 40, "saturatedFat": 14, "carbohydrates": 88,
            "sugars": 13, "protein": 32, "sodium": 1429,
        })
        self.recipe.refresh_from_db()
        n = self.recipe.nutrients
        self.assertEqual(n.energyKcal, 834)
        self.assertEqual(n.fat, 40)
        self.assertEqual(n.fatSaturated, 14)
        self.assertEqual(n.carbs, 88)
        self.assertEqual(n.sugar, 13)
        self.assertEqual(n.protein, 32)
        # UK/EU convention: salt (g) = sodium (mg) * 2.5 / 1000, rounded
        self.assertEqual(n.salt, 4)

    def test_no_page_nutrition_leaves_recipe_without_nutrients(self):
        self.scraper.create_nutrients(self.recipe, None)
        self.recipe.refresh_from_db()
        self.assertIsNone(self.recipe.nutrients)

    def test_page_nutrition_with_only_servingsize_leaves_recipe_without_nutrients(self):
        # this is what Mob's page data looks like when it genuinely has no macros recorded
        self.scraper.create_nutrients(self.recipe, {"servingSize": 2})
        self.recipe.refresh_from_db()
        self.assertIsNone(self.recipe.nutrients)
