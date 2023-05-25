from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
import json

from Apps.MealManager.services.Scraper.scraper import get_scraper



@permission_classes([IsAuthenticated])
@api_view(['GET'])
@swagger_auto_schema()
def get_status(request):
    return HttpResponse(json.dumps(get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def start_scraper(request):
    get_scraper().start()
    return HttpResponse(json.dumps(get_scraper().get_status()), content_type='application/json')


@api_view(['POST'])
@swagger_auto_schema()
def stop_scraper(request):
    get_scraper().stop()
    return HttpResponse(json.dumps(get_scraper().get_status()), content_type='application/json')

@api_view(['POST'])
@swagger_auto_schema()
def restart_scraper(request):
    get_scraper().restart()
    return HttpResponse(json.dumps(get_scraper().get_status()), content_type='application/json')

@api_view(['POST'])
@swagger_auto_schema()
def set_index(request, index):
    get_scraper().set_progress(index)
    return HttpResponse(json.dumps(get_scraper().get_status()), content_type='application/json')
