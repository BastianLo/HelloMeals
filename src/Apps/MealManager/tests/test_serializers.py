from django.contrib.auth.models import User
from django.db.models import FloatField, Value
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate

from Apps.MealManager.models import Recipe
from Apps.MealManager.serializers import RecipeBaseSerializer


def _authenticated_request(query_params=None):
    factory = APIRequestFactory()
    django_request = factory.get("/api/Recipe/x", query_params or {})
    user = User.objects.create_user(username="serializer-test-user", password="test-pass-123")
    force_authenticate(django_request, user=user)
    return Request(django_request)


class RecipeBaseSerializerSimilarityTests(TestCase):
    """Covers the crash fixed in serializers.py: get_similarity/get_relevancy used to call
    obj.calculate_similarity(...), a method that doesn't exist on Recipe, and even accessing
    obj.similarity directly raised AttributeError whenever the instance wasn't annotated with
    it - which RecipeBaseDetail's plain queryset never does (only RecipeFilterSet.filter_search
    does, and that's only wired into RecipeBaseList)."""

    def setUp(self):
        self.recipe = Recipe.objects.create(helloFreshId="r1", name="Test Recipe")

    def test_similarity_and_relevancy_are_none_without_search(self):
        request = _authenticated_request()
        data = RecipeBaseSerializer(self.recipe, context={"request": request}).data
        self.assertIsNone(data["similarity"])
        self.assertIsNone(data["relevancy"])

    def test_similarity_does_not_crash_when_not_annotated(self):
        request = _authenticated_request({"srch": "pasta"})
        data = RecipeBaseSerializer(self.recipe, context={"request": request}).data
        self.assertIsNone(data["similarity"])
        self.assertIsNone(data["relevancy"])

    def test_similarity_returned_when_queryset_annotated(self):
        annotated_recipe = Recipe.objects.annotate(
            similarity=Value(0.8, output_field=FloatField()),
            relevancy=Value(4.2, output_field=FloatField()),
        ).get(pk=self.recipe.pk)
        request = _authenticated_request({"srch": "pasta"})
        data = RecipeBaseSerializer(annotated_recipe, context={"request": request}).data
        self.assertEqual(data["similarity"], 0.8)
        self.assertEqual(data["relevancy"], 4.2)
