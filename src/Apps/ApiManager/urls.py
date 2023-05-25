from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import os

from .views import scraperView, recipeView

schema_view = get_schema_view(
    openapi.Info(
        title="HelloMeals Swagger",
        default_version='v1',
        description="API Documentation for HelloMeals",
        contact=openapi.Contact(url="https://github.com/BastianLo/HelloMeals"),
        license=openapi.License(name="Apache-2.0 license "),
    ),
    url=os.getenv("APP_URL", "http://127.0.0.1:8000"),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('', RedirectView.as_view(url='swagger/')),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('FullRecipe', recipeView.RecipeFullList.as_view()),
    path('FullRecipe/<str:helloFreshId>', recipeView.RecipeFullDetail.as_view()),

    path('Recipe', recipeView.RecipeBaseList.as_view()),
    path('Recipe/<str:helloFreshId>', recipeView.RecipeBaseDetail.as_view()),

    path('Cuisine', recipeView.CuisineList.as_view()),

    path('Scraper/status', scraperView.get_status),
    path('Scraper/start', scraperView.start_scraper),
    path('Scraper/stop', scraperView.stop_scraper),
    path('Scraper/restart', scraperView.restart_scraper),
    path('Scraper/setprogress/<int:index>', scraperView.set_index),

]