from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
import json

from Apps.MealManager.services.Scraper import scraper, scraperKitchenStories


### HelloFresh Scraper ###
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
def get_status(request):
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def start_scraper(request):
    scraper.get_scraper().start()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def stop_scraper(request):
    scraper.get_scraper().stop()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def restart_scraper(request):
    scraper.get_scraper().restart()
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def set_index(request, index):
    scraper.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraper.get_scraper().get_status()), content_type='application/json')


### KitchenStories Scraper ###

@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
def get_kitchen_stories_status(request):
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def start_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().start()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def stop_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().stop()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def restart_kitchen_stories_scraper(request):
    scraperKitchenStories.get_scraper().restart()
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def set_kitchen_stories_index(request, index):
    scraperKitchenStories.get_scraper().set_progress(index)
    return HttpResponse(json.dumps(scraperKitchenStories.get_scraper().get_status()), content_type='application/json')
