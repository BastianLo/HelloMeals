from dj_rql.filter_cls import RQLFilterClass, AutoRQLFilterClass
from dj_rql.qs import NSR

from .models import Recipe, Cuisine

class RecipeFilters(AutoRQLFilterClass):
    MODEL = Recipe

    FILTERS = [
        {
            'filter': 'protein',
            'source': 'nutrients__protein',
        },
        {
            'filter': 'kj',
            'source': 'nutrients__energyKj',
        },
        {
            'filter': 'kcal',
            'source': 'nutrients__energyKcal',
        },
        {
            'filter': 'fat',
            'source': 'nutrients__fat',
        },
        {
            'filter': 'fatSat',
            'source': 'nutrients__fatSaturated',
        },
        {
            'filter': 'carbs',
            'source': 'nutrients__carbs',
        },
        {
            'filter': 'sugar',
            'source': 'nutrients__sugar',
        },
        {
            'filter': 'salt',
            'source': 'nutrients__salt',
        },
    ]
    class Meta:
        fields = '__all__'

class CuisineFilters(AutoRQLFilterClass):
    MODEL = Cuisine