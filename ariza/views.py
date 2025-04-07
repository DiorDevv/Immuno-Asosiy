from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from dori.models import CustomPagination
from .permissions import ArizaPermission
from .serializers import *


class TransplantCenterViewSet(viewsets.ModelViewSet):
    queryset = TransplantCenter.objects.all()
    serializer_class = TransplantCenterSerializer
    permission_classes = [ArizaPermission,]


class ToWhomViewSet(viewsets.ModelViewSet):
    queryset = ToWhom.objects.all()
    serializer_class = ToWhomSerializer
    permission_classes = [ArizaPermission,]

# class ApplicationStatusViewSet(viewsets.ModelViewSet):
#     queryset = ApplicationStatus.objects.all()
#     serializer_class = ApplicationStatusSerializer
#     permission_classes = []

class MedicationTypeAppViewSet(viewsets.ModelViewSet):
    queryset = MedicationType.objects.all()
    serializer_class = MedicationTypeAppSerializer
    permission_classes = [ArizaPermission, ]

class MedicationAppViewSet(viewsets.ModelViewSet):
    queryset = MedicationApp.objects.all()
    serializer_class = MedicationAppSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['medication_type']
    permission_classes = [ArizaPermission, ]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'to_center', 'position']
    search_fields = ['director_name', 'main_center', 'subject']
    permission_classes = [ArizaPermission,]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer

    @action(detail=True, methods=['post'])
    def add_medication(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationMedicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(application=application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        status_id = request.data.get('status')

        if status_id:
            new_status = get_object_or_404(ApplicationStatus, id=status_id)
            application.status = new_status
            application.save()
            return Response({'status': 'Status updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Status ID required'}, status=status.HTTP_400_BAD_REQUEST)


