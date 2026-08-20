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


class RecipeExportMealieTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="r3", name="Export Test Recipe")
        self.client_ = authenticated_client(create_user("export-user"))

    def test_export_returns_html_with_json_ld(self):
        response = self.client_.get(f"/api/Recipe/{self.recipe.helloFreshId}/export/mealie")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text/html", response["Content-Type"])
        content = response.content.decode()
        self.assertIn('<script type="application/ld+json">', content)
        self.assertIn('"name": "Export Test Recipe"', content)

    def test_export_unknown_recipe_returns_404(self):
        response = self.client_.get("/api/Recipe/does-not-exist/export/mealie")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_export_requires_authentication(self):
        response = APIClient().get(f"/api/Recipe/{self.recipe.helloFreshId}/export/mealie")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


class RecipeShareLinkTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="r4", name="Share Test Recipe")
        self.client_ = authenticated_client(create_user("share-user"))

    def test_share_link_requires_authentication(self):
        response = APIClient().get(f"/api/Recipe/{self.recipe.helloFreshId}/share-link")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_share_link_unknown_recipe_returns_404(self):
        response = self.client_.get("/api/Recipe/does-not-exist/share-link")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_link_points_to_a_working_public_url(self):
        response = self.client_.get(f"/api/Recipe/{self.recipe.helloFreshId}/share-link")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        share_url = response.json()["url"]
        self.assertIn("/api/Recipe/shared/", share_url)

        # the shared URL must work for a fully anonymous client - no bearer token at all
        path = share_url.split("/api", 1)[1]
        anon_response = APIClient().get("/api" + path)
        self.assertEqual(anon_response.status_code, status.HTTP_200_OK)
        self.assertIn('"name": "Share Test Recipe"', anon_response.content.decode())

    def test_shared_endpoint_rejects_invalid_token(self):
        response = APIClient().get("/api/Recipe/shared/not-a-real-token")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
