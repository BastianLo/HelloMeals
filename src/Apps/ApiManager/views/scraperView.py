import json

from Apps.MealManager.services.Scraper import scraper, scraperKitchenStories, scraperChefKoch, scraperLecker, \
    scraperEatSmarter
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


### HelloFresh Scraper ###

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_status(request):
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_scraper(request):
    scraper.get_scraper().start()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_scraper(request):
    scraper.get_scraper().stop()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_scraper(request):
    scraper.get_scraper().restart()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_index(request, index):
    scraper.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


### KitchenStories Scraper ###

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_kitchen_stories_status(request):
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().start()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().stop()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().restart()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_kitchen_stories_index(request, index):
    scraperKitchenStories.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


### ChefKoch Scraper ###

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_chefkoch_status(request):
    return HttpResponse(json.dumps(scraperChefKoch.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_chefkoch_scraper(request):
    scraperChefKoch.get_scraper().start()
    return HttpResponse(json.dumps(scraperChefKoch.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_chefkoch_scraper(request):
    scraperChefKoch.get_scraper().stop()
    return HttpResponse(json.dumps(scraperChefKoch.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_chefkoch_scraper(request):
    scraperChefKoch.get_scraper().restart()
    return HttpResponse(json.dumps(scraperChefKoch.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_chefkoch_index(request, index):
    scraperChefKoch.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraperChefKoch.get_scraper().get_status()), content_type='application/json')


### Lecker Scraper ###

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_lecker_status(request):
    return HttpResponse(json.dumps(scraperLecker.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_lecker_scraper(request):
    scraperLecker.get_scraper().start()
    return HttpResponse(json.dumps(scraperLecker.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_lecker_scraper(request):
    scraperLecker.get_scraper().stop()
    return HttpResponse(json.dumps(scraperLecker.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_lecker_scraper(request):
    scraperLecker.get_scraper().restart()
    return HttpResponse(json.dumps(scraperLecker.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_lecker_index(request, index):
    scraperLecker.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraperLecker.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_status(request):
    response = {
        "Chefkoch": scraperChefKoch.get_scraper().get_status(),
        "KitchenStories": scraperKitchenStories.get_scraper().get_status(),
        "HelloFresh": scraper.get_scraper().get_status(),
        "Lecker": scraperLecker.get_scraper().get_status(),
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


### EatSmarter Scraper ###

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_es_status(request):
    return HttpResponse(json.dumps(scraperEatSmarter.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def start_es_scraper(request):
    scraperEatSmarter.get_scraper().start()
    return HttpResponse(json.dumps(scraperEatSmarter.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def stop_es_scraper(request):
    scraperEatSmarter.get_scraper().stop()
    return HttpResponse(json.dumps(scraperEatSmarter.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def restart_es_scraper(request):
    scraperEatSmarter.get_scraper().restart()
    return HttpResponse(json.dumps(scraperEatSmarter.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['POST'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def set_es_index(request, index):
    scraperEatSmarter.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraperEatSmarter.get_scraper().get_status()), content_type='application/json')


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@api_view(['GET'])
@swagger_auto_schema()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_status(request):
    response = {
        "Chefkoch": scraperChefKoch.get_scraper().get_status(),
        "KitchenStories": scraperKitchenStories.get_scraper().get_status(),
        "HelloFresh": scraper.get_scraper().get_status(),
        "Lecker": scraperLecker.get_scraper().get_status(),
        "EatSmarter": scraperEatSmarter.get_scraper().get_status(),
    }
    return HttpResponse(json.dumps(response), content_type='application/json')
