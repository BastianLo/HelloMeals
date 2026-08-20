from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Apps.MealManager.models import Recipe

from .utils import authenticated_client, create_user


class RecipeFavoriteTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="r1", name="Test Recipe")
        self.user = create_user("fav-user")
        self.client_ = authenticated_client(self.user)

    def test_set_favorite_true_adds_user(self):
        response = self.client_.post(f"/api/Recipe/{self.recipe.helloFreshId}/favorite/true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.recipe.favoriteBy.filter(pk=self.user.pk).exists())

    def test_set_favorite_false_removes_user(self):
        self.recipe.favoriteBy.add(self.user)
        response = self.client_.post(f"/api/Recipe/{self.recipe.helloFreshId}/favorite/false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.recipe.favoriteBy.filter(pk=self.user.pk).exists())

    def test_set_favorite_requires_authentication(self):
        response = APIClient().post(f"/api/Recipe/{self.recipe.helloFreshId}/favorite/true")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_set_favorite_unknown_recipe_returns_404(self):
        response = self.client_.post("/api/Recipe/does-not-exist/favorite/true")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RecipeBaseDetailSearchRegressionTests(TestCase):
    def test_detail_with_srch_param_does_not_crash(self):
        # Regression test for the serializers.py fix - this endpoint used to 500 whenever a
        # ?srch= param was present, since RecipeBaseDetail never annotates .similarity.
        recipe = Recipe.objects.create(helloFreshId="r2", name="Test Recipe 2")
        client = authenticated_client(create_user("detail-user"))
        response = client.get(f"/api/Recipe/{recipe.helloFreshId}?srch=pasta")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json()["similarity"])


class RecipeBaseListTests(TestCase):
    def test_requires_authentication(self):
        response = APIClient().get("/api/Recipe")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_filter_by_source(self):
        Recipe.objects.create(
            helloFreshId="hf1", name="HelloFresh Recipe", source=Recipe.Source.hellofresh,
            averageRating=4, ratingCount=10,
        )
        Recipe.objects.create(
            helloFreshId="mob1", name="Mob Recipe", source=Recipe.Source.mob,
            averageRating=4, ratingCount=10,
        )
        client = authenticated_client(create_user("list-user"))

        response = client.get(f"/api/Recipe?source={Recipe.Source.mob}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {r["helloFreshId"] for r in response.json()["results"]}
        self.assertIn("mob1", ids)
        self.assertNotIn("hf1", ids)
