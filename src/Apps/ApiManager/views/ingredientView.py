import django_filters
from Apps.MealManager.models import Ingredient
from Apps.MealManager.serializers import IngredientSerializer
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F, FloatField, ExpressionWrapper
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from util.pagination import RqlPagination


class IngredientFilterSet(filters.FilterSet):
    srch = django_filters.CharFilter(method='filter_search')
    relevancy = django_filters.CharFilter(method='filter_relevancy')

    def filter_search(self, queryset, name, value):
        return queryset.annotate(
            similarity=(TrigramSimilarity('name', value))
        ).filter(similarity__gt=0.3).annotate(
            relevancy=ExpressionWrapper(
                F('similarity'),
                output_field=FloatField()
            )
        ).order_by('-relevancy')

    def filter_relevancy(self, queryset, name, value):
        return queryset.annotate(
            relevancy=F('rating') * F('ratingCount')
        ).order_by('-relevancy')

    class Meta:
        model = Ingredient
        fields = ['srch', 'relevancy']


@permission_classes([IsAuthenticated])
class IngredientList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    filterset_class = IngredientFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            fields = self.request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                meta = IngredientSerializer.Meta
                meta.exclude = None
                meta.fields = fields
                return type('DynamicRecipeBaseSerializer', (IngredientSerializer,), {'Meta': meta})
            else:
                return IngredientSerializer
        return IngredientSerializer

    def get_queryset(self):
        recipes = Ingredient.objects.filter(parent=None)
        return recipes
