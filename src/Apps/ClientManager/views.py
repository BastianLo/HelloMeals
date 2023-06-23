from Apps.MealManager.models import InviteToken
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


def get_base_context():
    return {}


def navigation_history(request):
    request.session['previous_url'] = request.META.get('HTTP_REFERER')


def back_view(request):
    previous_url = request.session.get('previous_url')
    if previous_url:
        return redirect(previous_url)
    else:
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
def settings_profile(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsProfile.html", context)


@staff_member_required
@login_required(login_url='/accounts/login/')
def settings_admin(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsAdmin.html", context)


@staff_member_required
@login_required(login_url='/accounts/login/')
def settings_invite(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsInvite.html", context)


@staff_member_required
@login_required(login_url='/accounts/login/')
def settings_grouping_index(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingIndex.html", context)


@staff_member_required
@login_required(login_url='/accounts/login/')
def settings_grouping_tag(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingTag.html", context)


@staff_member_required
@login_required(login_url='/accounts/login/')
def settings_grouping_ingredients(request):
    navigation_history(request)
    context = get_base_context()
    return render(request, "ClientManager/pages/Settings/SettingsGroupingIngredients.html", context)


@staff_member_required
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


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                form.add_error(None, "Ungültiger Benutzername oder Passwort")
        else:
            form.add_error(None, "Ungültiger Benutzername oder Passwort")

    else:
        form = AuthenticationForm(request)
    return render(request, 'ClientManager/pages/registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def registration_view(request, token):
    try:
        invite_token = InviteToken.objects.get(id=token)
    except InviteToken.DoesNotExist:
        return render(request, 'ClientManager/pages/registration/registrationInvalidToken.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            invite_token.delete()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'ClientManager/pages/registration/registration.html', {'form': form})
