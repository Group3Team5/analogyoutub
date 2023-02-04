from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import *


class RegAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        data = {}
        data['response'] = True

        return Response(data, status=status.HTTP_200_OK)



