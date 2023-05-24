from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="recipe_index"),
    path("Recipe/", views.recipe_overview),
]