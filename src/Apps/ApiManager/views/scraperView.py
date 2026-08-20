import json

from Apps.MealManager.services.Scraper import scraper, scraperKitchenStories, scraperChefKoch, scraperLecker, \
    scraperEatSmarter, scraperMob
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Single source of truth for every recipe-source scraper: its URL key, the display name used
# in the combined status response, and the module exposing get_scraper(). Adding a new scraper
# only means adding a row here - the views below and the url patterns are generic.
SCRAPER_REGISTRY = [
    ("hellofresh", "HelloFresh", scraper),
    ("kitchenstories", "KitchenStories", scraperKitchenStories),
    ("chefkoch", "Chefkoch", scraperChefKoch),
    ("lecker", "Lecker", scraperLecker),
    ("eatsmarter", "EatSmarter", scraperEatSmarter),
    ("mob", "Mob", scraperMob),
]
SCRAPERS = {key: module for key, _, module in SCRAPER_REGISTRY}


def _json_response(data, status=200):
    return HttpResponse(json.dumps(data), status=status, content_type='application/json')


def _get_scraper_or_404(source):
    module = SCRAPERS.get(source)
    if module is None:
        return None, _json_response({"error": f"Unknown scraper source '{source}'"}, status=404)
    return module.get_scraper(), None


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_scraper_status(request, source):
    scraper_instance, error = _get_scraper_or_404(source)
    if error:
        return error
    return _json_response(scraper_instance.get_status())


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_scraper(request, source):
    scraper_instance, error = _get_scraper_or_404(source)
    if error:
        return error
    scraper_instance.start()
    return _json_response(scraper_instance.get_status())


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_scraper(request, source):
    scraper_instance, error = _get_scraper_or_404(source)
    if error:
        return error
    scraper_instance.stop()
    return _json_response(scraper_instance.get_status())


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_scraper(request, source):
    scraper_instance, error = _get_scraper_or_404(source)
    if error:
        return error
    scraper_instance.restart()
    return _json_response(scraper_instance.get_status())


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_scraper_index(request, source, index):
    scraper_instance, error = _get_scraper_or_404(source)
    if error:
        return error
    scraper_instance.set_progress(index)
    return _json_response(scraper_instance.get_status())


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_status(request):
    response = {
        display_name: module.get_scraper().get_status()
        for key, display_name, module in SCRAPER_REGISTRY
    }
    return _json_response(response)
