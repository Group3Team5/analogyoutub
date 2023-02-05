from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer


class ChatsAPI(GenericAPIView):
    serializer_class = ChatSerializer

    def get(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            response['chats'] = ChatSerializer().\
                chat_list(Chat.objects.all().filter(is_private=False))
            response['response'] = True
            return Response(response, status=status.HTTP_200_OK)
        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            serializer = ChatSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response['response'] = True
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response['errors'] = serializer.errors
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ChatAPI(GenericAPIView):

    def get(self, request, chat):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                chat = Chat.objects.get(slug__contains=chat)
                response['chat'] = ChatSerializer().chat_info(chat)
                response['messages'] = MessageSerializer().message_list(Message.objects.all().filter(chat_id=chat.id))
                response['response'] = True
                return Response(response, status=status.HTTP_200_OK)
            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class MessagesAPI(GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request, chat):
        user = request.user

        response = {}

        if user.is_authenticated:
            try:
                chat = Chat.objects.get(slug__contains=chat)
                response['chat'] = ChatSerializer().chat_info(chat)
                response['messages'] = MessageSerializer().message_list(Message.objects.all().filter(chat_id=chat.id))
                response['response'] = True
                return Response(response, status=status.HTTP_200_OK)
            except:
                response['response'] = False
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, chat):
        user = request.user

        response = {}

        if user.is_authenticated:

            for i in request.data:
                print(i)

            try:
                c = Chat.objects.get(slug__contains=chat)

                if len(request.data['text']) > 0 and\
                        len(c.subscribes.filter(username=user.username)) == 1:
                    message = Message.objects.create(
                        text=request.data['text'],
                        sender=user,
                        chat=c
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


class LinkAPI(GenericAPIView):
    pass
