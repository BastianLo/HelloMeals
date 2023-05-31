from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import os

from .views import scraperView, recipeView, tagView

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

    path('Tag/Merge', tagView.TagMergeListCreate.as_view()),
    path('Tag/Group', tagView.TagGroupList.as_view()),
    path('Tag', tagView.TagListCreate.as_view()),
    path('Tag/Full', tagView.TagGroupFullList.as_view()),
    path('Tag/<str:helloFreshId>', tagView.TagDetail.as_view()),

    path('Scraper/status', scraperView.get_all_status),

    path('Scraper/hellofresh/status', scraperView.get_status),
    path('Scraper/hellofresh/start', scraperView.start_scraper),
    path('Scraper/hellofresh/stop', scraperView.stop_scraper),
    path('Scraper/hellofresh/restart', scraperView.restart_scraper),
    path('Scraper/hellofresh/setprogress/<int:index>', scraperView.set_index),

    path('Scraper/kitchenstories/status', scraperView.get_kitchen_stories_status),
    path('Scraper/kitchenstories/start', scraperView.start_kitchen_stories_scraper),
    path('Scraper/kitchenstories/stop', scraperView.stop_kitchen_stories_scraper),
    path('Scraper/kitchenstories/restart', scraperView.restart_kitchen_stories_scraper),
    path('Scraper/kitchenstories/setprogress/<int:index>', scraperView.set_kitchen_stories_index),

    path('Scraper/chefkoch/status', scraperView.get_chefkoch_status),
    path('Scraper/chefkoch/start', scraperView.start_chefkoch_scraper),
    path('Scraper/chefkoch/stop', scraperView.stop_chefkoch_scraper),
    path('Scraper/chefkoch/restart', scraperView.restart_chefkoch_scraper),
    path('Scraper/chefkoch/setprogress/<int:index>', scraperView.set_chefkoch_index),

]