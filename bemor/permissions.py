from rest_framework.permissions import BasePermission

class BemorPermission(BasePermission):
    """
    Faqat 'vrach' ro‘liga ega foydalanuvchilar CRUD amallarini bajarishi mumkin.
    Boshqa foydalanuvchilar faqat GET (Read) imkoniyatiga ega bo‘ladi.
    """

    def has_permission(self, request, view):
        user = request.user

        # Foydalanuvchi autentifikatsiya qilinganmi?
        if not user or not user.is_authenticated:
            return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin

        # Foydalanuvchi "vrach" ro‘liga egami?
        if hasattr(user, "role_user") and user.role_user.lower() == "vrach":
            return True  # ✅ CRUD amallariga ruxsat beriladi

        return request.method in ["GET", "HEAD", "OPTIONS"]  # ❌ Faqat o‘qish mumkin
