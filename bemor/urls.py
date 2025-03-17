from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BemorQoshishCreateView, ManzilViewSet, OperatsiyaBolganJoyViewSet, \
    BemorViewSet, ExportBemorExcelView

# ViewSet-lar uchun Router yaratamiz
router = DefaultRouter()
router.register(r'manzil', ManzilViewSet, basename='manzil')

router.register(r'operatsiyalar', OperatsiyaBolganJoyViewSet)
router.register(r'bemorlar', BemorViewSet)
urlpatterns = [
    path('bemor-qoshish/', BemorQoshishCreateView.as_view(), name='bemor-qoshish'),
    path("export/bemorlar/", ExportBemorExcelView.as_view(), name="export_bemorlar"),

    # ManzilViewSet API-lari uchun avtomatik URL-larni qo‘shamiz
    path('', include(router.urls)),
]
