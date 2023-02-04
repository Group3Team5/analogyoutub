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

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password2': ["Пароль не совпадает"]})
        user.set_password(password)
        user.save()
        return user







