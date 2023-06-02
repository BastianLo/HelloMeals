import django_filters
from Apps.MealManager.models import Recipe
from Apps.MealManager.serializers import RecipeFullSerializer, RecipeBaseSerializer
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
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
    ingredient_count__lt = django_filters.NumberFilter(
        method='filter_ingredient_count',
        label='Ingredient Count less than',
    )

    def filter_search(self, queryset, name, value):
        return queryset.annotate(
            similarity=(TrigramSimilarity('name', value) * 5 + TrigramSimilarity('description', value))
        ).filter(similarity__gt=0.5).order_by('-similarity')

    def filter_ingredient_count(self, queryset, name, value):
        return queryset.annotate(
            ingredient_count=Count('recipeingredient')
        ).filter(ingredient_count__lte=value)

    class Meta:
        model = Recipe
        fields = ['srch', 'tag', 'cloned_from_null', 'difficulty', 'ingredient_count__lt']
        ordering_fields = '__all__'

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


@permission_classes([IsAuthenticated])
class RecipeBaseList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
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
        queryset = self.filter_tags()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            fields = ordering.split(',')
            queryset = queryset.order_by(*fields)
        return queryset

@permission_classes([IsAuthenticated])
class RecipeBaseDetail(generics.RetrieveAPIView):
    serializer_class = RecipeBaseSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Recipe.objects.all()
