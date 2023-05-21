from django.shortcuts import render
from django.http import HttpResponse
from .services.Scraper import scraper
# Create your views here.


def index(request):
    scraper.scrape(0)
    return HttpResponse("return this string")