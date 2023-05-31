import django_filters

from Apps.MealManager.models import Recipe


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    search = django_filters.CharFilter(method='perform_search')

    def perform_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    class Meta:
        model = Recipe
        fields = ['title', 'search']