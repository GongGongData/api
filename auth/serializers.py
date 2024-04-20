from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UuidUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login']
        read_only_fields = ['last_login']
