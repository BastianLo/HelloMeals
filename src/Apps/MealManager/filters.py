from dj_rql.filter_cls import RQLFilterClass, AutoRQLFilterClass

from .models import Recipe, Cuisine

class RecipeFilters(AutoRQLFilterClass):
    MODEL = Recipe

class CuisineFilters(AutoRQLFilterClass):
    MODEL = Cuisine