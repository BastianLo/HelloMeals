from dj_rql.filter_cls import RQLFilterClass, AutoRQLFilterClass
from .models import Recipe


class RecipeFilters(AutoRQLFilterClass):
    MODEL = Recipe