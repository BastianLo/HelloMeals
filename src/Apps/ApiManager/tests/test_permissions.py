from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Apps.MealManager.models import Ingredient, InviteToken, Recipe, Tag

from .utils import authenticated_client, create_admin, create_user

ANON_REJECTED = (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


class DecoratorCleanupPermissionRegressionTests(TestCase):
    """Regression coverage for removing the dead-looking @permission_classes(...) class
    decorators from ApiManager views. Two of them (TagMergeListCreate, InviteListCreate)
    weren't actually dead: the decorator ran *after* the class body and silently overwrote a
    weaker `permission_classes = [IsAuthenticated]` set in the body with the decorator's
    `[IsAuthenticated, IsAdminUser]` - so the real, previously-effective permission was the
    stricter one. These tests pin that down so a future cleanup can't quietly loosen it again."""

    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="r1", name="Test")
        self.regular = create_user("regular")
        self.admin = create_admin()

    def test_recipe_full_detail_requires_authentication(self):
        response = APIClient().get(f"/api/FullRecipe/{self.recipe.helloFreshId}")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_recipe_base_detail_requires_authentication(self):
        response = APIClient().get(f"/api/Recipe/{self.recipe.helloFreshId}")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_tag_detail_requires_authentication(self):
        tag = Tag.objects.create(helloFreshId="t1", type="x", name="Tag 1")
        response = APIClient().get(f"/api/Tag/{tag.helloFreshId}")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_tag_group_full_list_requires_authentication(self):
        response = APIClient().get("/api/Tag/Full")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_invite_list_requires_admin_not_just_authenticated(self):
        client = authenticated_client(self.regular)
        response = client.get("/api/auth/invites/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_list_allows_admin(self):
        client = authenticated_client(self.admin)
        response = client.get("/api/auth/invites/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invite_detail_requires_admin_not_just_authenticated(self):
        invite = InviteToken.objects.create(issuer=self.admin)
        client = authenticated_client(self.regular)
        response = client.get(f"/api/auth/invites/{invite.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_merge_list_requires_admin_not_just_authenticated(self):
        client = authenticated_client(self.regular)
        response = client.get("/api/Tag/Merge")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_merge_list_allows_admin(self):
        client = authenticated_client(self.admin)
        response = client.get("/api/Tag/Merge")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_user_requires_authentication(self):
        response = APIClient().get("/api/auth/me/")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_current_user_works_when_authenticated(self):
        client = authenticated_client(self.regular)
        response = client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "regular")

    def test_change_membership_requires_authentication(self):
        response = APIClient().post("/api/Stock/1/Membership")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_remove_membership_requires_authentication(self):
        response = APIClient().get("/api/Stock/Membership")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_add_ingredient_to_stock_requires_authentication(self):
        ingredient = Ingredient.objects.create(helloFreshId="i1", name="Salt")
        response = APIClient().post(f"/api/Ingredient/Stock/{ingredient.helloFreshId}")
        self.assertIn(response.status_code, ANON_REJECTED)

    def test_add_ingredient_to_shopping_list_requires_authentication(self):
        ingredient = Ingredient.objects.create(helloFreshId="i2", name="Pepper")
        response = APIClient().post(f"/api/Ingredient/ShoppingList/{ingredient.helloFreshId}")
        self.assertIn(response.status_code, ANON_REJECTED)
