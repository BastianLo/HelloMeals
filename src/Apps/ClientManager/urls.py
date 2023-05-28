from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from .views import back_view

urlpatterns = [
    path("", views.index, name="recipe_index"),
    path('back/', back_view, name='back_view'),

    path("Recipe/", views.recipe_overview),

    path("Settings/Index/", views.settings_index),
]