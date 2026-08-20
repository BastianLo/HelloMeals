import os

from HelloMeals.dynamic_preferences_registry import CustomGlobalPreferencesViewSet, CustomUserPreferencesViewSet
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import scraperView, recipeView, tagView, authentification_view, ingredientView, stockView

router = SimpleRouter()
router.register(r'global', CustomGlobalPreferencesViewSet, basename='global')
router.register(r'user', CustomUserPreferencesViewSet, basename='global')

schema_view = get_schema_view(
    openapi.Info(
        title="HelloMeals Swagger",
        default_version='v1',
        description="API Documentation for HelloMeals",
        contact=openapi.Contact(url="https://github.com/BastianLo/HelloMeals"),
        license=openapi.License(name="Apache-2.0 license "),
    ),
    url=os.getenv("APP_URL", "http://127.0.0.1:8000"),
    public=False,
    permission_classes=[permissions.IsAuthenticated, ],
)

urlpatterns = [
    path('', RedirectView.as_view(url='swagger/')),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('settings/', include(router.urls)),

    ### --- API Authentification --- ###
    path('auth/token/', authentification_view.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', authentification_view.RegisterView.as_view(), name='register_user'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/me/', authentification_view.current_user, name='current_user'),
    path('auth/refresh/', authentification_view.RefreshTokenView.as_view(), name='token_obtain_pair'),
    path('auth/invites/', authentification_view.InviteListCreate.as_view()),
    path('auth/invites/<str:id>', authentification_view.InviteDetail.as_view()),

    path('FullRecipe', recipeView.RecipeFullList.as_view()),
    path('FullRecipe/<str:helloFreshId>', recipeView.RecipeFullDetail.as_view()),

    path('Recipe', recipeView.RecipeBaseList.as_view()),
    path('Recipe/BaseInformation', recipeView.RecipeBaseInformationView.as_view()),
    path('Recipe/<str:helloFreshId>', recipeView.RecipeBaseDetail.as_view()),
    path('Recipe/<str:helloFreshId>/favorite/<str:favorite>', recipeView.set_favorite),

    path('Stock', stockView.StockListCreate.as_view()),
    path('Stock/<int:id>/Membership', stockView.change_membership),
    path('Stock/Membership', stockView.remove_membership),

    path('Ingredient', ingredientView.IngredientList.as_view()),
    path('Ingredient/Stock', ingredientView.stockList.as_view()),
    path('Ingredient/Stock/<str:ingredient_id>', ingredientView.add_ingredient_to_stock),
    path('Ingredient/ShoppingList', ingredientView.shoppingListView.as_view()),
    path('Ingredient/ShoppingList/<str:ingredient_id>', ingredientView.add_ingredient_to_shopping_list),
    path('Ingredient/<str:helloFreshId>/assign/<str:parentId>', ingredientView.assign_ingredient_parent),
    path('Ingredient/<str:helloFreshId>/assign/', ingredientView.assign_ingredient_parent),

    path('Tag/Merge', tagView.TagMergeListCreate.as_view()),
    path('Tag/Group', tagView.TagGroupList.as_view()),
    path('Tag', tagView.TagListCreate.as_view()),
    path('Tag/Full', tagView.TagGroupFullList.as_view()),
    path('Tag/<str:helloFreshId>', tagView.TagDetail.as_view()),

    path('Scraper/status', scraperView.get_all_status),
]

# One set of paths per registered scraper (see scraperView.SCRAPER_REGISTRY), all pointing at
# the same generic views with the source baked in as a fixed kwarg - keeps the URL strings
# identical to before without repeating them by hand for every source.
for _source in scraperView.SCRAPERS:
    urlpatterns += [
        path(f'Scraper/{_source}/status', scraperView.get_scraper_status, {'source': _source}),
        path(f'Scraper/{_source}/start', scraperView.start_scraper, {'source': _source}),
        path(f'Scraper/{_source}/stop', scraperView.stop_scraper, {'source': _source}),
        path(f'Scraper/{_source}/restart', scraperView.restart_scraper, {'source': _source}),
        path(f'Scraper/{_source}/setprogress/<int:index>', scraperView.set_scraper_index, {'source': _source}),
    ]
