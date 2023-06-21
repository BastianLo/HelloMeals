from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


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
def recipe_index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeIndex.html", context)


@login_required(login_url='/accounts/login/')
def recipe_overview(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeOverview.html", context)


@login_required(login_url='/accounts/login/')
def recipe_favorite(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeFavorites.html", context)


@login_required(login_url='/accounts/login/')
def recipe_details(request, recipe_id):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Recipes/RecipeDetails.html", context)


@login_required(login_url='/accounts/login/')
def stock_stock(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Stock/Stock.html", context)


@login_required(login_url='/accounts/login/')
def stock_shopping_list(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Stock/ShoppingList.html", context)


@login_required(login_url='/accounts/login/')
def settings_index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsIndex.html", context)


@login_required(login_url='/accounts/login/')
def settings_admin(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsAdmin.html", context)


@login_required(login_url='/accounts/login/')
def settings_grouping_index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingIndex.html", context)


@login_required(login_url='/accounts/login/')
def settings_grouping_tag(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingTag.html", context)


@login_required(login_url='/accounts/login/')
def settings_grouping_ingredients(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingIngredients.html", context)


@login_required(login_url='/accounts/login/')
def settings_downloader(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsDownloader.html", context)


def handler404(request, *args, **argv):
    response = render(request, 'ClientManager/errors/404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'ClientManager/errors/500.html', {})
    response.status_code = 500
    return response
