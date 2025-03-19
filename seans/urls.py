from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KorikModelViewSet



router = DefaultRouter()
router.register(r'', KorikModelViewSet)


urlpatterns = [
    path('', include(router.urls))
]
