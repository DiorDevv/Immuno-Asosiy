from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KorikModelViewSet, KorikPDFAPIView

router = DefaultRouter()
router.register(r'', KorikModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api/korik/<int:korik_id>/pdf/", KorikPDFAPIView.as_view(), name="korik_pdf_api"),

]
