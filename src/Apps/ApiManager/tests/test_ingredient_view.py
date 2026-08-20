from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Apps.MealManager.models import Ingredient

from .utils import authenticated_client, create_admin, create_user


class IngredientListTests(TestCase):
    def test_requires_authentication(self):
        response = APIClient().get("/api/Ingredient")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_lists_top_level_ingredients_only(self):
        parent = Ingredient.objects.create(helloFreshId="p", name="Tomato")
        Ingredient.objects.create(helloFreshId="c", name="Cherry Tomato", parent=parent)
        client = authenticated_client(create_user("ingredient-user"))

        response = client.get("/api/Ingredient")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {i["name"] for i in response.json()["results"]}
        self.assertIn("Tomato", names)
        self.assertNotIn("Cherry Tomato", names)


class AssignIngredientParentTests(TestCase):
    def setUp(self):
        self.admin = create_admin()
        self.client_ = authenticated_client(self.admin)
        self.a = Ingredient.objects.create(helloFreshId="a", name="A")
        self.b = Ingredient.objects.create(helloFreshId="b", name="B")

    def test_assign_parent(self):
        response = self.client_.post(f"/api/Ingredient/{self.a.helloFreshId}/assign/{self.b.helloFreshId}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.a.refresh_from_db()
        self.assertEqual(self.a.parent, self.b)

    def test_cannot_assign_a_parent_that_already_has_a_parent(self):
        self.b.parent = self.a
        self.b.save()
        other = Ingredient.objects.create(helloFreshId="c", name="C")

        response = self.client_.post(f"/api/Ingredient/{other.helloFreshId}/assign/{self.b.helloFreshId}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requires_admin(self):
        client = authenticated_client(create_user("regular"))
        response = client.post(f"/api/Ingredient/{self.a.helloFreshId}/assign/{self.b.helloFreshId}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
