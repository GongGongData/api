from rest_framework import serializers
from django.contrib.auth.models import User


class UuidUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login']


class UuidLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
