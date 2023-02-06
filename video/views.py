from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from video.models import Video, Comments, Subscribes
from video.serializers import VideoSerializer, CommentSerializer


class VideosAPI(GenericAPIView):
    serializer_class = VideoSerializer

    def get(self, request):
        user = request.user

        response = {}

        response['videos'] = VideoSerializer().video_list(
            Video.objects.all()
        )

        response['response'] = True
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            if len(request.data['name']) == 0:
                response['errors'] = {
                    'error': 'Поле name должно быть заполненным'
                }
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            elif len(Video.objects.filter(name=request.data['name']))== 0:
                Video.objects.create(
                    name=request.data['name'],
                    creator=user
                ).save()
                response['response'] = True
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response['errors'] = {
                    'error': 'Видео с таким названием уже существует'
                }
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class VideoAPI(GenericAPIView):

    def get(self, request, video):
        user = request.user

        response = {}

        v = Video.objects.filter(slug__contains=video)

        if len(v) > 0:
            response['video_info'] = VideoSerializer().video_info(v[0])
            response['comments'] = CommentSerializer().comment_list(
                Comments.objects.all().filter(video=v[0])
            )
            response['response'] = True
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['response'] = False
            response['error'] = 'Видео не существует'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommentsAPI(GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, video):
        user = request.user

        response = {}

        v = Video.objects.filter(slug__contains=video)

        if len(v) > 0:
            response['comments'] = CommentSerializer().comment_list(
                Comments.objects.all().filter(video=v[0])
            )
            response['response'] = True
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['response'] = False
            response['error'] = 'Видео не существует'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, video):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                c = Video.objects.get(slug__contains=video)



                if len(request.data['text']) > 0:
                    message = Comments.objects.create(
                        text=request.data['text'],
                        sender=user,
                        video=c
                    )
                    response['response'] = True
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    response['errors'] = {
                        "text": [
                            "This field may not be blank."
                        ]
                    }
                    response['response'] = False
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class LikeAPI(GenericAPIView):

    def get(self, request, video):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                video = Video.objects.get(slug__contains=video)

                if len(video.likes.filter(username=user.username)) == 0:
                    if len(video.dislikes.filter(username=user.username)) > 0:
                        video.dislikes.remove(user)
                    video.likes.add(user)
                else:
                    video.likes.remove(user)
                response['response'] = True
                return Response(response, status=status.HTTP_200_OK)

            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class DislikeAPI(GenericAPIView):

    def get(self, request, video):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                video = Video.objects.get(slug__contains=video)

                if len(video.dislikes.filter(username=user.username)) == 0:
                    if len(video.likes.filter(username=user.username)) > 0:
                        video.likes.remove(user)
                    video.dislikes.add(user)
                else:
                    video.dislikes.remove(user)
                response['response'] = True
                return Response(response, status=status.HTTP_200_OK)

            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class SubscribeAPI(GenericAPIView):
    def get(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                subscribes = Subscribes.objects.all().filter(users=user)
                creator = User.objects.get(username=request.data['creator'])

                if len(subscribes.filter(creator=creator)) == 0:
                    Subscribes.objects.create(
                        creator=creator,
                        users=user
                    ).save()
                else:
                    subscribes.filter(creator=creator).delete()

                print(len(subscribes.filter(creator=creator)))

                response['response'] = True
                return Response(response, status=status.HTTP_200_OK)

            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
