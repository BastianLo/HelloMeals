from django.shortcuts import render
from django.http import HttpResponse
from .services.Scraper import scraper
# Create your views here.


def index(request):
    for i in range(1):
        scraper.scrape(i)
    return HttpResponse("return this string")