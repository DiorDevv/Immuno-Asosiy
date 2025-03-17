
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Shifokor_qoshish, ShifokorModelViewSet


# ViewSet-lar uchun Router yaratamiz
router = DefaultRouter()
router.register(r'', ShifokorModelViewSet)

urlpatterns = [
    path('shaxsiy_malumotlar/', Shifokor_qoshish.as_view(), name='shaxsiy-malumotlar'),

    path('', include(router.urls)),
]
