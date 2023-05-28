from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


def get_base_context():
    return {}


def navigation_history(request):
    # Retrieve the navigation history list from the session
    ng = request.session.get('navigation_history', [])
    # Append the current URL to the history list
    ng.append(request.META.get('HTTP_REFERER'))
    # Limit the history list to a maximum number of URLs if desired
    max_history_length = 10  # Set your desired maximum history length
    ng = ng[-max_history_length:]
    # Update the session with the updated history list
    request.session['navigation_history'] = ng
    # Your view logic here


def back_view(request):
    # Retrieve the navigation history list from the session
    ng = request.session.get('navigation_history', [])
    if len(ng) > 1:
        # Remove the current URL from the history list
        ng.pop()
        # Get the previous URL from the updated history list
        previous_url = ng[-1]
        # Update the session with the updated history list
        request.session['navigation_history'] = ng
        # Redirect the user to the previous URL
        return redirect(previous_url)
    else:
        # Handle the case when there are no previous URLs available
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
