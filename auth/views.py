from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView
from .serializers import UuidUserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import *
from rest_framework.response import Response


# Create your views here.
class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UuidUserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
        })

    def post(self, request, *args, **kwargs):
        loginAttempt = request.POST["username"]

        user = authenticate(uuid=loginAttempt)
        login(request, user)
        return Response({
            "id": user.id,
            "username": user.username,
        })

    def delete(self, request, *args, **kwargs):
        userId = request.user.id
        username = request.user.username

        logout(request)
        return Response({
            "msg": "User logged out",
            "id": userId,
            "username": username,
        })
