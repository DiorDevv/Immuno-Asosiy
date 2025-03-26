from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.auth.hashers import identify_hasher
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

NEW, DONE = ('new', 'done',)

class Role(models.TextChoices):
    TTB = "TTB", "TTB"
    VSSB = "VSSB", "VSSB"
    UZMED = "UZMED", "UZMED"
    VAZIR = "Vazir", "Vazir"
    VRACH = "VRACH", "VRACH"


class CustomUser(AbstractUser, BaseModel):
    AUTH_STATUS = (
        (NEW, NEW),
        (DONE, DONE),
    )
    role_user = models.CharField(
        max_length=10, choices=Role.choices, default=Role.TTB
    )
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)

    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def check_username(self):
        if not self.username:
            while True:
                temp_username = f'Immuno-{get_random_string(6)}'
                if not CustomUser.objects.filter(username=temp_username).exists():
                    break
            self.username = temp_username

    def check_pass(self):
        if not self.password:
            temp_password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'
            self.set_password(temp_password)

    def hashing_password(self):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.set_password(self.password)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        if not self.pk:  # ❗ Faqat yangi foydalanuvchi yaratilganda chaqiramiz
            self.check_username()
            self.check_pass()
            self.hashing_password()
        super().save(*args, **kwargs)




