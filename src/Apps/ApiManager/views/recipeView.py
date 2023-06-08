import random

import django_filters
from Apps.MealManager.models import Recipe
from Apps.MealManager.serializers import RecipeFullSerializer, RecipeBaseSerializer
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count, F, FloatField, ExpressionWrapper, Q
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from util.pagination import RqlPagination


### Filter Sets ###

class RecipeFilterSet(filters.FilterSet):
    tag = filters.CharFilter(field_name='recipetag__tag__helloFreshId')
    cloned_from_null = filters.BooleanFilter(field_name='clonedFrom', lookup_expr='isnull')
    srch = django_filters.CharFilter(method='filter_search')
    difficulty = django_filters.NumberFilter(field_name='difficulty')
    recipeType = django_filters.NumberFilter(field_name='recipeType')
    ingredient_count__lt = django_filters.NumberFilter(
        method='filter_ingredient_count',
        label='Ingredient Count less than',
    )
    relevancy = django_filters.CharFilter(method='filter_relevancy')

    calories_gt = django_filters.NumberFilter(field_name='nutrients__energyKcal', lookup_expr='gt')
    calories_lt = django_filters.NumberFilter(field_name='nutrients__energyKcal', lookup_expr='lt')

    def filter_search(self, queryset, name, value):
        return queryset.annotate(
            similarity=(TrigramSimilarity('name', value) * 5 + Coalesce(TrigramSimilarity('description', value), 0.0,
                                                                        output_field=FloatField()))
        ).filter(similarity__gt=0.5).annotate(
            relevancy=ExpressionWrapper(
                F('similarity') * ((F('ratingCount') * F('averageRating')) ** 0.05),
                output_field=FloatField()
            )
        ).order_by('-relevancy')

    def filter_ingredient_count(self, queryset, name, value):
        return queryset.annotate(
            ingredient_count=Count('recipeingredient')
        ).filter(ingredient_count__lte=value)

    def filter_relevancy(self, queryset, name, value):
        return queryset.annotate(
            relevancy=F('rating') * F('ratingCount')
        ).order_by('-relevancy')

    class Meta:
        model = Recipe
        fields = ['srch', 'tag', 'cloned_from_null', 'difficulty', 'ingredient_count__lt', 'relevancy', 'calories_gt',
                  'calories_lt']


### Views ###

@permission_classes([IsAuthenticated])
class RecipeFullList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
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


class RecipeBaseList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = RecipeFilterSet
    pagination_class = RqlPagination
    queryset = Recipe.objects.all()

    def filter_tags(self, queryset):
        tags = self.request.GET.get('tags')
        if tags:
            tag_group = tags.split('@')
            for group in tag_group:
                tag_list = group.split('_')
                queryset = queryset.filter(recipetag__tag__helloFreshId__in=tag_list).distinct()
            return queryset
        return queryset

    def filter_source(self, queryset):
        tags = self.request.GET.get('source')
        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(source__in=tag_list).distinct()
            return queryset
        return queryset

    def filter_relevancy(self, queryset):
        queryset = queryset.annotate(relevancy=F('averageRating') * F('ratingCount'))
        ordering = self.request.query_params.get('ordering', None)
        if ordering == 'relevancy':
            queryset = queryset.order_by('-relevancy')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            fields = self.request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                meta = RecipeBaseSerializer.Meta
                meta.fields = fields
                return type('DynamicRecipeBaseSerializer', (RecipeBaseSerializer,), {'Meta': meta})
            else:
                return RecipeBaseSerializer
        return RecipeBaseSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.filter_tags(queryset)
        queryset = self.filter_source(queryset)
        queryset = queryset.filter(clonedFrom__isnull=True)
        queryset = queryset.exclude(Q(headline__contains="Inhalt"))
        queryset = queryset.annotate(relevance=F('averageRating') * F('ratingCount')).exclude(relevance=0)
        queryset = self.filter_relevancy(queryset)
        ordering = self.request.query_params.get('ordering', None)
        random_param = self.request.query_params.get('random')
        if random_param == 'true':
            sample_size = int(self.request.query_params.get('sample_size', 10))
            hellofresh_ids = queryset.values_list('recipetag__tag__helloFreshId', flat=True).distinct()
            random_hellofresh_ids = random.sample(list(hellofresh_ids), min(sample_size, len(hellofresh_ids)))
            queryset = queryset.filter(recipetag__tag__helloFreshId__in=random_hellofresh_ids)
        elif ordering and ordering != 'relevancy':
            fields = ordering.split(',')
            queryset = queryset.order_by(*fields)
        return queryset


@permission_classes([IsAuthenticated])
class RecipeBaseDetail(generics.RetrieveAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Recipe.objects.all()
