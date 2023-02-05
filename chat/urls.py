from django.urls import path
from chat.views import *


#back_end_api/chat/


urlpatterns = [
    path('', ChatsAPI.as_view()),
    path('<slug>/', ChatAPI.as_view()),
    path('<slug>/messages/', MessagesAPI.as_view()),
    path('<slug>/link/', LinkAPI.as_view()),
]
