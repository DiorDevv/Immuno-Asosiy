from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BemorQoshishCreateView, ManzilViewSet, OperatsiyaBolganJoyViewSet, \
    BemorViewSet, ExportBemorExcelView, BemorHolatiStatistika, BemorPDFDownloadView, \
    ViloyatViewSet

# ViewSet-lar uchun Router yaratamiz
router = DefaultRouter()
router.register(r'manzil', ManzilViewSet, basename='manzil')

router.register(r'operatsiyalar', OperatsiyaBolganJoyViewSet)
router.register(r'bemorlar', BemorViewSet, basename='bemorlar')
router.register(r'viloyat', ViloyatViewSet, basename='viloyat')

urlpatterns = [
    path('bemor-qoshish/', BemorQoshishCreateView.as_view(), name='bemor-qoshish'),
    path("export/bemorlar/", ExportBemorExcelView.as_view(), name="export_bemorlar"),
    path('bemor-statistika/', BemorHolatiStatistika.as_view(), name='bemor-holati-statistika'),
    path('bemor/<int:pk>/pdf/', BemorPDFDownloadView.as_view(), name='bemor-pdf-download'),

    # ManzilViewSet API-lari uchun avtomatik URL-larni qo‘shamiz
    path('', include(router.urls)),
]
