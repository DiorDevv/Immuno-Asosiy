from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicationTypeViewSet,
    MedicationViewSet,
    PatientViewSet,
    InventoryTransactionViewSet,
    NotificationViewSet, AttachmentViewSet, MedicationPrescriptionDetailView, PrescribedMedicationListCreateView

)

# Create a router for viewsets
router = DefaultRouter()

# Register viewsets with the router
router.register(r'medication-types', MedicationTypeViewSet, basename='medicationtype')
# router.register(r'doriii', DoriWiew)
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'inventory-transactions', InventoryTransactionViewSet, basename='inventorytransaction')
router.register(r'notifications', NotificationViewSet)
router.register(r'attachments', AttachmentViewSet)

# Define URL patterns
urlpatterns = [
    # Include router URLs for viewsets
    path('', include(router.urls)),

    # URLs for MedicationPrescription views

    path(
        'medication-prescriptions/<int:pk>/',
        MedicationPrescriptionDetailView.as_view(),
        name='medicationprescription-detail'
    ),
path(
        'tavsiya_etilgan_dori/',
        PrescribedMedicationListCreateView.as_view(),
        name='tavsiya_etilgan_dorilar'
    ),

    # URLs for PrescribedMedication views

    # path(
    #     'prescribed-medications/<int:pk>/',
    #     PrescribedMedicationDetailView.as_view(),
    #     name='prescribedmedication-detail'
    # ),
]
