from django.urls import path
from chat.views import *


#back_end_api/chat/


urlpatterns = [
    path('', ChatsAPI.as_view()),
    path('<str:chat>/', ChatAPI.as_view()),
    path('<str:chat>/messages/', MessagesAPI.as_view()),
    path('<str:chat>/link/', LinkAPI.as_view()),
]
