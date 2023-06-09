from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from .views import back_view

urlpatterns = [
    path("", views.index, name="recipe_index"),
    path('back/', back_view, name='back_view'),

    path("Recipe/", views.recipe_index, name="recipe.overview"),
    path("Recipe/All", views.recipe_overview, name="recipe.all"),
    path("Recipe/Favorites", views.recipe_favorite, name="recipe.favorites"),
    path("Recipe/<str:recipe_id>/", views.recipe_details),

    path("Settings/", RedirectView.as_view(url='/Home/Settings/Index/')),
    path("Settings/Index/", views.settings_index),
    path("Settings/Downloader/", views.settings_downloader, name="settings.downloader"),
    path("Settings/Profile/", views.settings_index, name="settings.profile"),
    path("Settings/Grouping/", views.settings_grouping_index, name="settings.grouping"),
    path("Settings/Grouping/Tag", views.settings_grouping_tag, name="settings.grouping.tag"),
    path("Settings/Grouping/Ingredient", views.settings_grouping_index, name="settings.grouping.ingredient"),
]
