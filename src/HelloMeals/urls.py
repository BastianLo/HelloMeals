"""
URL configuration for HelloMeals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.views.i18n import set_language, JavaScriptCatalog

from . import settings

urlpatterns = [
    path('adminPage/', admin.site.urls),
    path('set-language/', set_language, name='set_language'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('pwa.urls')),
    path('accounts/', include("Apps.ClientManager.urls"), name='login'),

    path("", RedirectView.as_view(url='/Home/')),
    path("api/", include("Apps.ApiManager.urls")),
    path('Home/', include("Apps.ClientManager.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'Apps.ClientManager.views.handler404'
handler500 = 'Apps.ClientManager.views.handler500'
