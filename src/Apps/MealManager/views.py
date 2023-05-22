from django.http import HttpResponse
from .services.Scraper.scraper import get_scraper
# Create your views here.


def index(request):
    return HttpResponse("return this string")