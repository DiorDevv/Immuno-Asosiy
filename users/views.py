from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import generics, permissions

from users.models import User
from users.serializers import SignUpSerializer, LoginSerializer #LoginRefreshSerializer

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
#
#
# class LoginRefreshView(TokenRefreshView):
#     serializer_class = LoginRefreshSerializer
