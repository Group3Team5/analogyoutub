from django.urls import path
from frontend.views import *

urlpatterns = [
    path('', redirect_window),

    path('login/', login_window),
    path('reg/', reg_window),


    path('video/', videos_page),
    path('video/subscribes/', sub_page),
    path('video/likes/', l_page),
    path('video/dislikes/', d_page),
    path('video/create/', create),
    path('video/load_video/', load),
    path('video/user_video/<str:name>/', videos_page),
    path('video/<str:video>', video_page),

    path('chat/', chat_page),

    path('stream/<str:slug>/', get_streaming_video, name='stream'),

    path('swagger/', swagger, name='stream'),
]
