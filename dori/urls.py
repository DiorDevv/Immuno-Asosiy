# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Patient URLs
    # path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    # path('patients/<int:pk>/', views.PatientUpdateDestroyView.as_view(), name='patient-update-destroy'),

    # Medicine URLs
    path('medicines/', views.MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('medicines/<int:pk>/', views.MedicineUpdateDestroyView.as_view(), name='medicine-update-destroy'),

    # DoriQabulQilish URLs
    path('dori-qabul/', views.DoriQabulQilishListCreateView.as_view(), name='doriqabul-list-create'),
    path('dori-qabul/<int:pk>/', views.DoriQabulQilishUpdateDestroyView.as_view(), name='doriqabul-update-destroy'),

    # DoriQabulYakun URLs
    path('dori-yakun/', views.DoriQabulYakunListCreateView.as_view(), name='doriyakun-list-create'),
    path('dori-yakun/<int:pk>/', views.DoriQabulYakunUpdateDestroyView.as_view(), name='doriyakun-update-destroy'),

    # Patient Medicines URL
    path('patients/<int:pk>/medicines/', views.PatientMedicineListView.as_view(), name='patient-medicines'),
]