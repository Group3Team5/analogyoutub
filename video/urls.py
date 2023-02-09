from django.urls import path
from video.views import *


#back_end_api/video/


urlpatterns = [
    path('', VideosAPI.as_view()),

    path('subscribe/', SubscribeAPI.as_view()),
    path('<str:video>/', VideoAPI.as_view()),
    path('<str:video>/comments/', CommentsAPI.as_view()),
    path('<str:video>/like/', LikeAPI.as_view()),
    path('<str:video>/dislike/', DislikeAPI.as_view()),
]