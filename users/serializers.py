from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import Role, CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as DjangoUser


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    token = serializers.SerializerMethodField()
    role_user = serializers.ChoiceField(choices=Role.choices, required=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "token", "role_user")
        extra_kwargs = {"id": {"read_only": True}}

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username allaqachon mavjud.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")
        return value

    def create(self, validated_data):
        if not validated_data.get("username"):
            while True:
                temp_username = f"user_{get_random_string(6)}"
                if not CustomUser.objects.filter(username=temp_username).exists():
                    validated_data["username"] = temp_username
                    break

        validated_data["password"] = make_password(validated_data["password"])
        user = super().create(validated_data)
        return user

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    auth_status = serializers.CharField(read_only=True)
    role_user = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = CustomUser.objects.filter(username=username).first()
        print(user)
        if user is None:
            raise ValidationError({
                'success': False,
                'message': _("Kiritgan login yoki parolingiz noto‘g‘ri. Iltimos qayta tekshirib ko‘ring!")
            })

        if user.auth_status.lower() == "new":
            user.auth_status = "done"
            user.save()

        if user.auth_status.lower() == "new":
            raise ValidationError({
                'success': False,
                'message': _("Siz ro'yhatdan to'liq o'tmagansiz!")
            })

        if not user.is_active:
            raise ValidationError({
                'success': False,
                'message': _("Sizning hisobingiz faollashtirilmagan.")
            })

        self.user = user
        self.role_user = user.role_user

        return {
            "username": user.username,
            "full_name": user.get_full_name(),
            "auth_status": user.auth_status,
            "role_user": user.role_user,
            "token": self.get_token(user)["access"],
            'refresh_token': self.get_token(user)["refresh"],
        }

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["token"] = self.get_token(self.user)["access"]
        data["full_name"] = self.user.get_full_name()
        data["auth_status"] = self.user.auth_status
        data["role_user"] = self.role_user
        return data

#
# class LoginRefreshSerializer(TokenRefreshSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         access_token_instance = AccessToken(data['access'])
#
#         # user_id ni UUID ga aylantirish
#         try:
#             user_id = uuid.UUID(str(access_token_instance['user_id']))
#         except ValueError:
#             raise serializers.ValidationError("User ID noto‘g‘ri formatda")
#
#         user = get_object_or_404(User, id=user_id)
#         update_last_login(None, user)
#         return data
