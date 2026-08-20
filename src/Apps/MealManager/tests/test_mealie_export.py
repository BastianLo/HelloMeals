import json
from datetime import timedelta

from django.test import TestCase

from Apps.MealManager.models import (
    Ingredient,
    IngredientGroup,
    Nutrients,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Tag,
    WorkSteps,
)
from Apps.MealManager.services.mealie_export import build_recipe_html, build_recipe_json_ld


def _extract_json_ld(html_doc):
    start = html_doc.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
    end = html_doc.index("</script>", start)
    return json.loads(html_doc[start:end])


class BuildRecipeJsonLdTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            helloFreshId="r1",
            name="Tomatensuppe",
            description="Eine leckere Suppe",
            author="Chef Test",
            servings=4,
            prepTime=timedelta(minutes=15),
            totalTime=timedelta(minutes=45),
            websiteLink="https://example.com/tomatensuppe",
            averageRating=4.5,
            ratingCount=10,
        )
        group = IngredientGroup.objects.create(id="g1", name=None, related_recipe=self.recipe)
        tomato = Ingredient.objects.create(helloFreshId="i1", name="Tomaten")
        salt = Ingredient.objects.create(helloFreshId="i2", name="Salz")
        RecipeIngredient.objects.create(id="ri1", ingredient_group=group, ingredient=tomato, amount=500, unit="g")
        RecipeIngredient.objects.create(id="ri2", ingredient_group=group, ingredient=salt, amount=None, unit=None)
        WorkSteps.objects.create(id="w1", relatedRecipe=self.recipe, index=0, description="Tomaten schneiden.")
        WorkSteps.objects.create(id="w2", relatedRecipe=self.recipe, index=1, description="Alles köcheln lassen.")
        tag = Tag.objects.create(helloFreshId="t1", type="category", name="Hauptgericht")
        RecipeTag.objects.create(id="rt1", recipe=self.recipe, tag=tag)
        nutrients = Nutrients.objects.create(id="n1", energyKcal=120, protein=3, carbs=15, fat=2)
        self.recipe.nutrients = nutrients
        self.recipe.save()

    def test_basic_fields(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertEqual(data["@type"], "Recipe")
        self.assertEqual(data["name"], "Tomatensuppe")
        self.assertEqual(data["description"], "Eine leckere Suppe")
        self.assertEqual(data["author"], {"@type": "Person", "name": "Chef Test"})
        self.assertEqual(data["recipeYield"], "4")
        self.assertEqual(data["url"], "https://example.com/tomatensuppe")

    def test_durations_are_iso8601(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertEqual(data["prepTime"], "PT15M")
        self.assertEqual(data["totalTime"], "PT45M")

    def test_ingredients_formatted_with_amount_unit_name(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertIn("500 g Tomaten", data["recipeIngredient"])
        self.assertIn("Salz", data["recipeIngredient"])

    def test_instructions_in_order(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertEqual(
            [s["text"] for s in data["recipeInstructions"]],
            ["Tomaten schneiden.", "Alles köcheln lassen."],
        )

    def test_tags_become_keywords_and_category(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertIn("Hauptgericht", data["keywords"])
        self.assertEqual(data["recipeCategory"], "Hauptgericht")

    def test_nutrition(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertEqual(data["nutrition"]["calories"], "120 kcal")
        self.assertEqual(data["nutrition"]["proteinContent"], "3 g")

    def test_aggregate_rating(self):
        data = build_recipe_json_ld(self.recipe)
        self.assertEqual(data["aggregateRating"]["ratingCount"], 10)

    def test_missing_optional_fields_are_omitted_not_crashing(self):
        bare = Recipe.objects.create(helloFreshId="r2", name="Nacktes Rezept")
        data = build_recipe_json_ld(bare)
        self.assertEqual(data["name"], "Nacktes Rezept")
        self.assertNotIn("recipeIngredient", data)
        self.assertNotIn("recipeInstructions", data)
        self.assertNotIn("nutrition", data)
        self.assertNotIn("aggregateRating", data)

    def test_html_wraps_valid_json_ld(self):
        html_doc = build_recipe_html(self.recipe)
        self.assertIn('<script type="application/ld+json">', html_doc)
        parsed = _extract_json_ld(html_doc)
        self.assertEqual(parsed["name"], "Tomatensuppe")


class ImageUrlTests(TestCase):
    """Regression coverage: the image must always be a fully-qualified absolute URL - a local
    Django media path like "/media/images/recipes/x.jpg" is meaningless to Mealie, which has no
    page origin to resolve a relative URL against when HTML is pasted rather than fetched."""

    def test_prefers_external_source_image_when_present(self):
        recipe = Recipe.objects.create(
            helloFreshId="r3", name="Mit externem Bild",
            HelloFreshImageUrl="https://example.com/original.jpg",
        )
        data = build_recipe_json_ld(recipe, build_absolute_uri=lambda path: "http://SHOULD-NOT-BE-USED" + path)
        self.assertEqual(data["image"], ["https://example.com/original.jpg"])

    def test_falls_back_to_absolute_local_image_when_no_external_url(self):
        recipe = Recipe.objects.create(helloFreshId="r4", name="Ohne externes Bild")
        # simulate a locally-downloaded image without touching storage
        recipe.image.name = "images/recipes/local.jpg"
        data = build_recipe_json_ld(
            recipe, build_absolute_uri=lambda path: "https://hellomeals.example" + path
        )
        self.assertEqual(data["image"], ["https://hellomeals.example/media/images/recipes/local.jpg"])

    def test_no_image_when_neither_available(self):
        recipe = Recipe.objects.create(helloFreshId="r5", name="Ganz ohne Bild")
        data = build_recipe_json_ld(recipe, build_absolute_uri=lambda path: "https://x" + path)
        self.assertNotIn("image", data)
