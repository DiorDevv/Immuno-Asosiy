from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'centers', TransplantCenterViewSet)
router.register(r'positions', ToWhomViewSet)
# router.register(r'statuses', ApplicationStatusViewSet)
router.register(r'medication-types', MedicationTypeAppViewSet)
router.register(r'medications', MedicationAppViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]