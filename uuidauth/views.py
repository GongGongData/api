from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView
from .serializers import UuidUserSerializer, UuidLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json


# Create your views here.
class LoginView(APIView):
    serializer_class = UuidUserSerializer

    @swagger_auto_schema(operation_summary="로그인 확인")
    def get(self, request, *args, **kwargs):
        seri = UuidUserSerializer(request.user)
        return Response(seri.data)

    @csrf_exempt
    @swagger_auto_schema(operation_summary="로그인 or 회원가입",
                         request_body=UuidLoginSerializer,
                         responses={201: UuidUserSerializer})
    def post(self, request, *args, **kwargs):
        if (request.user.is_authenticated):
            return Response(UuidUserSerializer(request.user).data)

        loginAttempt = request.data['username']
        user = authenticate(uuid=loginAttempt)
        login(request, user)

        return Response(UuidUserSerializer(user).data, 201)

    @swagger_auto_schema(operation_summary="로그아웃")
    def delete(self, request, *args, **kwargs):
        userId = request.user.id
        username = request.user.username

        logout(request)
        return Response({
            "msg": "User logged out",
            "id": userId,
            "username": username,
        })
