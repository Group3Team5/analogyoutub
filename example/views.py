from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    message = "Example Django project on vercel"
    return HttpResponse(message)
