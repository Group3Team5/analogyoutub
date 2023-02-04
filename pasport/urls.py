from django.urls import path
from pasport.views import *

urlpatterns = [
    path('user/', RegAPIView.as_view()),
]