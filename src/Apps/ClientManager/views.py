from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    context = {}
    return render(request, "ClientManager/base.html", context)