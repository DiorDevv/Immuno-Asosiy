from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from bemor.models import Bemor
from bemor.serializers import BemorSerializer
from dori.models import Dori
from .serializers import PatientSerializer, MedicineSerializer

class PatientListView(APIView):
    def get(self, request):
        patients = Bemor.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientDetailView(APIView):
    def get(self, request, pk):
        patient = get_object_or_404(Bemor, pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientMedicineListView(APIView):
    def get(self, request, pk):
        patient = get_object_or_404(Bemor, pk=pk)
        medicines = patient.medicines.all()
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BemorDoriQabulAPIView(APIView):
    def get(self, request, bemor_id):
        bemor = get_object_or_404(Bemor, id=bemor_id)
        serializer = BemorSerializer(bemor)
        return Response(serializer.data, status=status.HTTP_200_OK)