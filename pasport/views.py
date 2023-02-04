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
            user_data['username'] = user.name
            user_data['email'] = user.email
        else:
            user_data['username'] = 'Anonymos'

        response['user'] = user_data
        response['response'] = True

        return Response(response, status=status.HTTP_200_OK)


class RegAPI(GenericAPIView):
    pass


class LoginAPI(GenericAPIView):
    pass



