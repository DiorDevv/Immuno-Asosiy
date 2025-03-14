from django.urls import path
from .views import PatientListView, PatientDetailView, PatientMedicineListView

urlpatterns = [
    path("patients/", PatientListView.as_view(), name="patient-list"),
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),
    path("patients/<int:pk>/medicines/", PatientMedicineListView.as_view(), name="patient-medicines"),
]
