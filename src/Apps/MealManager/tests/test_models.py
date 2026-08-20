from django.test import TestCase

from Apps.MealManager.models import Ingredient, Recipe


class IngredientManagerTests(TestCase):
    def test_update_or_create_dedups_by_name(self):
        first, created_first = Ingredient.objects.update_or_create(
            helloFreshId="a1", defaults={"name": "Tomato"}
        )
        self.assertTrue(created_first)

        second, created_second = Ingredient.objects.update_or_create(
            helloFreshId="a2", defaults={"name": "Tomato"}
        )
        self.assertFalse(created_second)
        self.assertEqual(second.pk, first.pk)
        self.assertEqual(Ingredient.objects.count(), 1)


class IngredientHierarchyTests(TestCase):
    def setUp(self):
        self.parent = Ingredient.objects.create(helloFreshId="p", name="Tomato")
        self.child = Ingredient.objects.create(helloFreshId="c", name="Cherry Tomato", parent=self.parent)
        self.grandchild = Ingredient.objects.create(
            helloFreshId="g", name="Baby Cherry Tomato", parent=self.child
        )

    def test_get_descendants_includes_self_and_children_by_default(self):
        descendants = {i.helloFreshId for i in self.parent.get_descendants()}
        self.assertEqual(descendants, {"p", "c", "g"})

    def test_get_descendants_can_exclude_self(self):
        descendants = {i.helloFreshId for i in self.parent.get_descendants(include_self=False)}
        self.assertEqual(descendants, {"c", "g"})


class RecipeSourceChoicesTests(TestCase):
    def test_choices_match_expected_scraper_mapping(self):
        self.assertEqual(Recipe.Source.hellofresh, 1)
        self.assertEqual(Recipe.Source.kitchenstories, 2)
        self.assertEqual(Recipe.Source.chefkoch, 3)
        self.assertEqual(Recipe.Source.lecker, 4)
        self.assertEqual(Recipe.Source.eatsmarter, 5)
        self.assertEqual(Recipe.Source.yazio, 6)
        self.assertEqual(Recipe.Source.mob, 7)

    def test_default_source_is_hellofresh(self):
        recipe = Recipe.objects.create(helloFreshId="r1", name="Test Recipe")
        self.assertEqual(recipe.source, Recipe.Source.hellofresh)
