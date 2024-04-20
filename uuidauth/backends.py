from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class UuidBackend(BaseBackend):
    def authenticate(self, request, uuid=None):
        try:
            user = User.objects.get(username=uuid)
        except User.DoesNotExist:
            user = User(username=uuid)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
