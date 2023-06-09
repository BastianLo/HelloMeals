from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from .views import back_view

urlpatterns = [
    path("", views.index, name="recipe_index"),
    path('back/', back_view, name='back_view'),

    path("login/", views.login_view, name="auth.login"),
    path("logout/", views.logout_view, name="auth.logout"),
    path('register/<str:token>/', views.registration_view, name='register'),

    path("Stock/", views.recipe_index, name="stock.overview"),
    path("Stock/Stock", views.stock_stock, name="stock.stock"),
    path("Stock/Shoppinglist", views.stock_shopping_list, name="stock.shoppinglist"),

    path("Recipe/", views.recipe_index, name="recipe.overview"),
    path("Recipe/All", views.recipe_overview, name="recipe.all"),
    path("Recipe/Favorites", views.recipe_favorite, name="recipe.favorites"),
    path("Recipe/<str:recipe_id>/", views.recipe_details),

    path("Settings/", RedirectView.as_view(url='/Home/Settings/Index/')),
    # todo: implement actual view
    path("Settings/User", views.settings_index, name="settings.usersettings"),

    path("Settings/Profile/", views.settings_profile, name="settings.profile"),
    path("Settings/Index/", views.settings_index),
    path("Settings/Admin", views.settings_admin, name="settings.admin"),
    # todo: Implement actual view
    path("Settings/Admin/Global/", views.settings_admin, name="settings.global"),
    path("Settings/Admin/Invite/", views.settings_invite, name="settings.invite"),
    path("Settings/Admin/Downloader/", views.settings_downloader, name="settings.downloader"),
    path("Settings/Admin/Grouping/", views.settings_grouping_index, name="settings.grouping"),
    path("Settings/Admin/Grouping/Tag", views.settings_grouping_tag, name="settings.grouping.tag"),
    path("Settings/Admin/Grouping/Ingredient", views.settings_grouping_ingredients,
         name="settings.grouping.ingredient"),
]
