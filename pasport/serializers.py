from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password',
                  'password2']









