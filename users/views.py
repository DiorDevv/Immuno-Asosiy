from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .models import CustomUser
from .serializers import SignUpSerializer, LoginSerializer


class CreateUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
