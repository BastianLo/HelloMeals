from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


def get_base_context():
    return {}


@login_required(login_url='/accounts/login/')
def index(request):
    context = get_base_context()
    return render(request, "ClientManager/index.html", context)


@login_required(login_url='/accounts/login/')
def recipe_overview(request):
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeOverview.html", context)
