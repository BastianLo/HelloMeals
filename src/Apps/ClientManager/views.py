from django.http import HttpResponse
from django.shortcuts import render, redirect

def get_base_context():
    return {}

def index(request):
    context = get_base_context()
    return render(request, "ClientManager/index.html", context)

def recipe_overview(request):
    context = get_base_context()
    if 'HTTP_HX_REQUEST' in request.META:
        return render(request, "ClientManager/components/pageComponents/RecipeOverview.html", context)
    else:
        return render(request, "ClientManager/pages/Recipes/RecipeOverview.html", context)