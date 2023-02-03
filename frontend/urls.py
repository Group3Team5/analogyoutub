from django.urls import path
from frontend.views import *

urlpatterns = [
    path('', redirect_window),

    path('video/', video_page),
]