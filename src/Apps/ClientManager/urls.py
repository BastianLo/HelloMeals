from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from .views import back_view

urlpatterns = [
    path("", views.index, name="recipe_index"),
    path('back/', back_view, name='back_view'),

    path("Recipe/", views.recipe_overview),

    path("Settings/", RedirectView.as_view(url='/Home/Settings/Index/')),
    path("Settings/Index/", views.settings_index),
    path("Settings/Downloader/", views.settings_index, name="settings.downloader"),
    path("Settings/Profile/", views.settings_index, name="settings.profile"),
    path("Settings/Grouping/", views.settings_index, name="settings.grouping"),
]