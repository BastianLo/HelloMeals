from dj_rql.filter_cls import RQLFilterClass, AutoRQLFilterClass
from .models import Recipe

from .models import Recipe

class CuisineFilterCls(RQLFilterClass):
    def filter_by_cuisine(self, queryset, field, value):
        return queryset.filter(recipecuisine__cuisine__name=value)

    def get_filters(self):
        return {
            'cuisine.name': self.filter_by_cuisine,
        }

class RecipeFilters(AutoRQLFilterClass):
    MODEL = Recipe