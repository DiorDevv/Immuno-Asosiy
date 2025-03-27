from rest_framework.permissions import BasePermission
from users.models import Role  # Role modelingizni import qiling

class BemorPermission(BasePermission):
    """
    Faqat VRACH ro‘liga ega foydalanuvchilar CRUD (Create, Update, Delete) amallarini bajarishi mumkin.
    Boshqa foydalanuvchilar faqat GET (Read) imkoniyatiga ega bo‘ladi.
    """

    def has_permission(self, request, view):
        user = request.user

        # Foydalanuvchi autentifikatsiya qilinganmi?
        if not user or not user.is_authenticated:
            return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin

        # Foydalanuvchining roli "VRACH" ekanligini tekshirish
        user_role = getattr(user, "role_user", "").upper()

        if user_role == Role.VRACH:
            return True  # ✅ CRUD amallariga ruxsat beriladi

        return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin
