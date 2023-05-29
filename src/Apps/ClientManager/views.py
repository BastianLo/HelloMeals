from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


def get_base_context():
    return {}


def navigation_history(request):
    request.session['previous_url'] = request.META.get('HTTP_REFERER')

def back_view(request):
    # Retrieve the previous URL from the session
    previous_url = request.session.get('previous_url')
    if previous_url:
        # Redirect the user to the previous URL
        return redirect(previous_url)
    else:
        # Handle the case when there is no previous URL available
        return HttpResponse("Previous URL not found.")

@login_required(login_url='/accounts/login/')
def index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/index.html", context)


@login_required(login_url='/accounts/login/')
def recipe_overview(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeOverview.html", context)


@login_required(login_url='/accounts/login/')
def settings_index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsIndex.html", context)

@login_required(login_url='/accounts/login/')
def settings_downloader(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsDownloader.html", context)
