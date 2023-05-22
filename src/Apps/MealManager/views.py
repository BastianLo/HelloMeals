from django.http import HttpResponse
from .services.Scraper.scraper import get_scraper
# Create your views here.


def index(request):
    if False:
        if get_scraper().is_running():
            get_scraper().stop()
        else:
            get_scraper().start()
    else:
        get_scraper().scrape(0)
    return HttpResponse("return this string")