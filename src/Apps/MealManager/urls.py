from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='recipe')),
    path("recipe/", views.index, name="recipe_index"),
]