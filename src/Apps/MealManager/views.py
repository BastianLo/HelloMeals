from django.shortcuts import render
from django.http import HttpResponse
from .services.Scraper import scraper
# Create your views here.


def index(request):
    scraper.scrape()
    return HttpResponse("return this string")