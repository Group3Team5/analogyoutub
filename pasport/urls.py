from django.urls import path
from pasport.views import *

#back_end_api/pasport/




urlpatterns = [
    path('user/', UserAPI.as_view()),
    path('user/reg/', RegAPI.as_view()),
    path('user/login/', LoginAPI.as_view()),
]
