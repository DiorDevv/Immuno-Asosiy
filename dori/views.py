# views.py
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from bemor.models import Bemor  # Assuming this exists
from dori.models import Dori, DoriQabulQilish, DoriQabulYakun
from .serializers import (
    PatientSerializer,
    MedicineSerializer,
    DoriQabulQilishSerializer,
    DoriQabulYakunSerializer
)
#
# # Patient (Bemor) Views
# class PatientListCreateView(ListAPIView, CreateAPIView):
#     queryset = Bemor.objects.all()
#     serializer_class = PatientSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PatientUpdateDestroyView(UpdateAPIView, DestroyAPIView):
#     queryset = Bemor.objects.all()
#     serializer_class = PatientSerializer
#     lookup_field = 'pk'

# Medicine (Dori) Views
# class MedicineListCreateView(ListAPIView, CreateAPIView):
#     queryset = Dori.objects.all()
#     serializer_class = MedicineSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineListCreateView(ListAPIView):
    queryset = Dori.objects.all()
    serializer_class = MedicineSerializer

class MedicineUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = Dori.objects.all()
    serializer_class = MedicineSerializer
    lookup_field = 'pk'


# DoriQabulQilish Views
class DoriQabulQilishListCreateView(ListAPIView, CreateAPIView):
    queryset = DoriQabulQilish.objects.all()
    serializer_class = DoriQabulQilishSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoriQabulQilishUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = DoriQabulQilish.objects.all()
    serializer_class = DoriQabulQilishSerializer
    lookup_field = 'pk'

# DoriQabulYakun Views
class DoriQabulYakunListCreateView(ListAPIView, CreateAPIView):
    queryset = DoriQabulYakun.objects.all()
    serializer_class = DoriQabulYakunSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoriQabulYakunUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = DoriQabulYakun.objects.all()
    serializer_class = DoriQabulYakunSerializer
    lookup_field = 'pk'

# Additional View for Patient-Specific Medicines (assuming relationship exists)
class PatientMedicineListView(ListAPIView):
    serializer_class = MedicineSerializer

    def get_queryset(self):
        patient_id = self.kwargs['pk']
        return Dori.objects.filter(patients__id=patient_id)  # Assumes ManyToMany relationship