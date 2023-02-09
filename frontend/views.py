import os
from pathlib import Path
from wsgiref.util import FileWrapper

from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from djangoProject9.settings import VIDEOS_DIR
from frontend.services import open_file
from video.models import Video, Comments, Subscribes
from video.serializers import VideoSerializer, CommentSerializer


def redirect_window(request):
    return redirect("video/")

def l_page(request, name='a'):
    if not request.user.is_authenticated:
        return redirect('/login/')
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['title'] = 'Все видео'
    response['active_video'] = True

    if name == '':
        return redirect('/')
    else:
        r = VideoSerializer().video_list(
                Video.objects.filter(likes=request.user)
            )

    response['videos'] = [r[i] for i in r]

    return render(request, 'frontend/videos_page.html', response)


def d_page(request, name='a'):
    if not request.user.is_authenticated:
        return redirect('/login/')
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['title'] = 'Все видео'
    response['active_video'] = True

    if name == '':
        return redirect('/login/')
    else:
        r = VideoSerializer().video_list(
            Video.objects.filter(dislikes=request.user)
        )

    response['videos'] = [r[i] for i in r]

    return render(request, 'frontend/videos_page.html', response)


def videos_page(request, name=''):
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['title'] = 'Все видео'
    response['active_video'] = True

    if name == '':
        r = VideoSerializer().video_list(
                Video.objects.all()
            )
    else:
        r = VideoSerializer().video_list(
                Video.objects.filter(creator__username=name)
            )

    response['videos'] = [r[i] for i in r]

    return render(request, 'frontend/videos_page.html', response)


def video_page(request, video):
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['active_video'] = True

    try:
        v = Video.objects.get(slug__contains=video)
        response['video_empty'] = False
        response['title'] = v.name
        r = VideoSerializer().video_info(v)
        c = CommentSerializer().comment_list(Comments.objects.filter(video_id=v.id).order_by('created_date'))
        response['video'] = r
        response['comments'] = [c[i] for i in c]

        if request.user.is_authenticated:
            response['creator'] = v.creator.username
            response['likes'] = v.likes.count()
            response['dislikes'] = v.dislikes.count()
            response['sub'] = Subscribes.objects.filter(creator=v.creator, users=request.user).count() > 0

    except:
        response['video_empty'] = True
        response['title'] = 'Видео не существует'

    return render(request, 'frontend/video_page.html', response)


def chat_page(request):
    if request.user.is_authenticated:
        response = {}
        user_info = {
            'username': request.user.username,
            'is_authenticated': request.user.is_authenticated
        }
        response['user_info'] = user_info
        response['active_video'] = False
        response['title'] = 'Чат'

        return render(request, 'frontend/chat_page.html', response)
    return redirect('/login/')


def sub_page(request):
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['active_video'] = True

    if request.user.is_authenticated:
        subs = Subscribes.objects.filter(users=request.user)

        response['subs'] = [
            {'name':i.creator.username,
             's': Subscribes.objects.filter(creator=i.creator).count()}
            for i in subs
        ]

        response['subs_empty'] = len(response['subs']) == 0
        return render(request, 'frontend/subs.html', response)
    return redirect('/login/')


def login_window(request):
    if request.user.is_authenticated:
        return redirect('/video/')
    return render(request, 'frontend/login.html')

def reg_window(request):
    if request.user.is_authenticated:
        return redirect('/video/')
    return render(request, 'frontend/reg.html')



def get_streaming_video(request, slug: str):
    #file, status_code, content_length, content_range = open_file(request, slug)
    ch_s = 256
    filename=''
    try:
        path = os.path.join(VIDEOS_DIR, slug)
        for f in os.listdir(path):
            filename = f
        path = Path(os.path.join(path, filename))

        fw = FileWrapper(open(path, 'rb'), ch_s)

    except:
        path = os.path.join(VIDEOS_DIR, 'default')
        for f in os.listdir(path):
            filename = f
        path = Path(os.path.join(path, filename))
        fw = FileWrapper(open(path, 'rb'), ch_s)




    #response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4', bytes=1024)
    response = StreamingHttpResponse(fw, content_type='video/mp4')

    print(os.path.getsize(path))

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = os.path.getsize(path)
    response['Cache-Control'] = 'no-cache'
    return response

def swagger(request):
    return render(request, 'frontend/swagger.html')

def create(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    response = {}
    user_info = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
    response['user_info'] = user_info
    response['active_video'] = True
    return render(request, 'frontend/create.html', response)

@csrf_exempt
def load(request):
    try:
        print(1)
        path = os.path.join(VIDEOS_DIR, str(request.POST.get('slug')))
        for f in request.FILES:
            handle_uploaded_file(path, f, request.FILES[f])
            print(1)
    except:
        pass

    responce = HttpResponse()
    return responce


def handle_uploaded_file(path, filename, file):
    os.mkdir(path)
    path = os.path.join(path, filename)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
