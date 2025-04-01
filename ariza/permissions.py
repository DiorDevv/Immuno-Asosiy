from rest_framework.permissions import BasePermission

from users.models import Role


class ArizaPermission(BasePermission):
    """
    Faqat TTB ro‘liga ega foydalanuvchilar CRUD (Create, Update, Delete) amallarini bajarishi mumkin.
    Boshqa foydalanuvchilar faqat GET (Read) imkoniyatiga ega bo‘ladi.
    """

    def has_permission(self, request, view):
        user = request.user

        # Foydalanuvchi autentifikatsiya qilinganmi?
        if not user or not user.is_authenticated:
            return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin

        # Foydalanuvchining roli "VRACH" ekanligini tekshirish
        user_role = getattr(user, "role_user", "").upper()

        if user_role == Role.TTB:
            return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin

        return True  # ✅ CRUD amallariga ruxsat beriladi