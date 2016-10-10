from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Gyros Of Hummus test site. Trying to organize webhooks... It works")
