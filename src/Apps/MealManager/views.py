from django.http import HttpResponse
from .services.Scraper.scraper import get_scraper
# Create your views here.


def index(request):
    for i in range(10):
        get_scraper().scrape(i)
    return HttpResponse("return this string")