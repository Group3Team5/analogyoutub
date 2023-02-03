from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

def redirect_window(request):
    return redirect("video/")


def video_page(request):
    return render(request, 'frontend/video_page.html')
