from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import *


class UserAPI(GenericAPIView):

    def get(self, request):
        user = request.user

        response = {}
        user_data = {}

        response['is_authenticated'] = user.is_authenticated

        if user.is_authenticated:
            user_data['id'] = user.id
            user_data['username'] = user.username
            user_data['email'] = user.email
        else:
            user_data['username'] = 'Anonymos'

        response['user'] = user_data
        response['response'] = True

        return Response(response, status=status.HTTP_200_OK)


class RegAPI(GenericAPIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            response['response'] = False
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        serializer = UserRegSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response['response'] = True
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response['response'] = False
            response['errors'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(GenericAPIView):
    serializer_class = UserLoginSerializer

    def get(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            logout(request)
            response['response'] = True
            return Response(response, status=status.HTTP_200_OK)

        response['response'] = False
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user

        response = {}

        if user.is_authenticated:
            response['response'] = False
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            response['response'] = True
            user = authenticate(username=request.data['username'],
                                password=request.data['password'])
            login(request, user)
            return Response(response, status=status.HTTP_200_OK)

        response['errors'] = serializer.errors
        response['response'] = False
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
