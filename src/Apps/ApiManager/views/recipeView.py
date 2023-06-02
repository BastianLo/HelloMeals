from django_filters import rest_framework as filters
import django_filters
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from Apps.MealManager.serializers import RecipeFullSerializer, RecipeBaseSerializer
from Apps.MealManager.models import Recipe
from Apps.MealManager.filters import RecipeFilters

from util.pagination import RqlPagination


### Filter Sets ###

class RecipeFilterSet(filters.FilterSet):
    tag = filters.CharFilter(field_name='recipetag__tag__helloFreshId')

    srch = django_filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.annotate(
            similarity=(TrigramSimilarity('name', value) * 5 + TrigramSimilarity('description', value))
        ).filter(similarity__gt=0.5).order_by('-similarity')

    class Meta:
        model = Recipe
        fields = ['srch', 'tag']


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
    queryset = Recipe.objects.all()

    def filter_tags(self):
        tags = self.request.GET.get('tags')
        if tags:
            tag_group = tags.split('@')
            queryset = self.queryset
            for group in tag_group:
                tag_list = group.split('_')
                queryset = queryset.filter(recipetag__tag__helloFreshId__in=tag_list).distinct()
            return queryset
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeBaseSerializer
        return RecipeBaseSerializer

    def get_queryset(self):
        return self.filter_tags()


@permission_classes([IsAuthenticated])
class RecipeBaseDetail(generics.RetrieveAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Recipe.objects.all()
