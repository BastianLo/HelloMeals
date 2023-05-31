import django_filters

from Apps.MealManager.models import Recipe

class RecipeFilterSet(django_filters.FilterSet):
    difficulty = django_filters.NumberFilter(field_name='difficulty', lookup_expr='exact')
    isCloned = django_filters.BooleanFilter(field_name='clonedFrom', lookup_expr='isnull')

    class Meta:
        model = Recipe
        fields = ['difficulty']