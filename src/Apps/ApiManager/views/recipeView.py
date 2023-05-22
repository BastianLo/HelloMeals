from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.MealManager.serializers import RecipeFullSerializer, RecipeBaseSerializer, CuisineBaseSerializer
from Apps.MealManager.models import Recipe, Cuisine
from Apps.MealManager.filters import RecipeFilters, CuisineFilters

from util.pagination import RqlPagination


### Filter Sets ###

class RecipeFilterSet(filters.FilterSet):
    cuisine = filters.CharFilter(field_name='recipecuisine__cuisine__helloFreshId')
    tag = filters.CharFilter(field_name='recipetag__tag__helloFreshId')

    class Meta:
        model = Recipe
        fields = ['cuisine', 'tag']


### Views ###

@permission_classes([IsAuthenticated])
class RecipeFullList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    rql_filter_class = RecipeFilters
    filterset_class = RecipeFilterSet
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeFullSerializer
        return RecipeFullSerializer

    def get_queryset(self):
        recipes = Recipe.objects.all()
        return recipes


@permission_classes([IsAuthenticated])
class RecipeFullDetail(generics.RetrieveAPIView):
    serializer_class = RecipeFullSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Recipe.objects.all()


@permission_classes([IsAuthenticated])
class RecipeBaseList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    rql_filter_class = RecipeFilters
    filterset_class = RecipeFilterSet
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeBaseSerializer
        return RecipeBaseSerializer

    def get_queryset(self):
        recipes = Recipe.objects.all()
        return recipes


@permission_classes([IsAuthenticated])
class RecipeBaseDetail(generics.RetrieveAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Recipe.objects.all()


@permission_classes([IsAuthenticated])
class CuisineList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    rql_filter_class = CuisineFilters
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CuisineBaseSerializer
        return CuisineBaseSerializer

    def get_queryset(self):
        return Cuisine.objects.all()
