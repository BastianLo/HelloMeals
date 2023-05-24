from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control


def get_base_context():
    return {}


def index(request):
    context = get_base_context()
    return render(request, "ClientManager/index.html", context)

def recipe_overview(request):
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeOverview.html", context)
