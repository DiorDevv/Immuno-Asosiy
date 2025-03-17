from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicationTypeViewSet,
    MedicationViewSet,
    PatientViewSet,
    InventoryTransactionViewSet,
    MedicationPrescriptionListCreateView,
    MedicationPrescriptionDetailView,
    PrescribedMedicationListCreateView,
    PrescribedMedicationDetailView,

)

# Create a router for viewsets
router = DefaultRouter()

# Register viewsets with the router
router.register(r'/medication-types', MedicationTypeViewSet, basename='medicationtype')
# router.register(r'doriii', DoriWiew)
router.register(r'/medications', MedicationViewSet, basename='medication')
router.register(r'/patients', PatientViewSet, basename='patient')
router.register(r'/inventory-transactions', InventoryTransactionViewSet, basename='inventorytransaction')

# Define URL patterns
urlpatterns = [
    # Include router URLs for viewsets
    path('', include(router.urls)),

    # URLs for MedicationPrescription views
    path(
        'medication-prescriptions/',
        MedicationPrescriptionListCreateView.as_view(),
        name='medicationprescription-list-create'
    ),
    path(
        'medication-prescriptions/<int:pk>/',
        MedicationPrescriptionDetailView.as_view(),
        name='medicationprescription-detail'
    ),

    # URLs for PrescribedMedication views
    path(
        'prescribed-medications/',
        PrescribedMedicationListCreateView.as_view(),
        name='prescribedmedication-list-create'
    ),
    path(
        'prescribed-medications/<int:pk>/',
        PrescribedMedicationDetailView.as_view(),
        name='prescribedmedication-detail'
    ),
]
