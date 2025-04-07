
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from django.db.models import Sum, F, Q, IntegerField, Subquery
from django.http import HttpResponse, FileResponse
import pandas as pd
from rest_framework.parsers import MultiPartParser, FormParser

from datetime import datetime
from django.utils.timezone import make_aware
from .models import MedicationType, Medication, InventoryTransaction, Bemor, MedicationDetails, Notification, \
    Attachment, CustomPagination
from .permissions import DoriPermission
from .serializers import (
    MedicationTypeSerializer,
    MedicationSerializer,
    MedicationDetailSerializer,
    InventoryTransactionSerializer,
    MedicationDetailsSerializer, NotificationDetailSerializer, NotificationListSerializer, AttachmentSerializer
)
from .models import MedicationPrescription, TavsiyaEtilganDori
from .serializers import MedicationPrescriptionSerializer, TavsiyaEtilganDoriModelSerializer
from bemor.serializers import BemorSerializer

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import QabulQilishYakuniy
from .serializers import QabulQilishYakuniySerializer

class MedicationTypeViewSet(viewsets.ModelViewSet):
    queryset = MedicationType.objects.all()
    serializer_class = MedicationTypeSerializer
    permission_classes = [DoriPermission,]

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    filter_backends = [filters.SearchFilter]
    permission_classes = [DoriPermission,]
    search_fields = ['name', 'type__name']

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MedicationDetailSerializer
        return MedicationSerializer

    def get_queryset(self):
        queryset = Medication.objects.all()

        # Filter by medication type if provided
        medication_type = self.request.query_params.get('type')
        if medication_type:
            queryset = queryset.filter(type__name__icontains=medication_type)

        # Filter by name if provided
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get detailed information about a medication"""
        medication = self.get_object()
        try:
            details = medication.details
            serializer = MedicationDetailsSerializer(details)
            return Response(serializer.data)
        except MedicationDetails.DoesNotExist:
            return Response({"detail": "No detailed information available"}, status=404)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Bemor.objects.all()
    serializer_class = BemorSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [DoriPermission,]
    search_fields = ['first_name', 'last_name', 'patient_id']

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']

    @action(detail=True, methods=['get'])
    def medications(self, request, pk=None):
        """Get all medications assigned to a patient"""
        patient = self.get_object()
        transactions = patient.medication_transactions.all()

        # Group by medication
        medication_data = {}
        for transaction in transactions:
            med_id = transaction.medication.id
            if med_id not in medication_data:
                medication_data[med_id] = {
                    'medication': transaction.medication,
                    'total_quantity': 0,
                    'transactions': []
                }

            medication_data[med_id]['transactions'].append(transaction)
            if transaction.transaction_type == 'OUTPUT':
                medication_data[med_id]['total_quantity'] += transaction.quantity

        # Serialize the data
        result = []
        for med_data in medication_data.values():
            medication_serializer = MedicationSerializer(med_data['medication'])
            transaction_serializer = InventoryTransactionSerializer(med_data['transactions'], many=True)

            result.append({
                'medication': medication_serializer.data,
                'total_quantity': med_data['total_quantity'],
                'transactions': transaction_serializer.data
            })

        return Response(result)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryTransactionSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [DoriPermission,]
    pagination_class = CustomPagination
    search_fields = ['medication__name', 'medication__type__name', 'notes',
                     'patient__first_name', 'patient__last_name']

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = InventoryTransaction.objects.all()

        # Filter by archived status
        archived = self.request.query_params.get('archived')
        if archived == 'true':
            queryset = queryset.filter(archived=True)
        elif archived == 'false' or archived is None:
            queryset = queryset.filter(archived=False)

        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset





class DoriQabulQilishViewSet(viewsets.ModelViewSet):
    queryset = QabulQilishYakuniy.objects.all()
    serializer_class = QabulQilishYakuniySerializer
    permission_classes = [DoriPermission,]
    pagination_class = CustomPagination
    # Limit to GET and POST methods
    http_method_names = ['get', 'post']


class NotificationViewSet(viewsets.ModelViewSet):
    """API endpoint for notifications"""
    queryset = Notification.objects.all()
    filterset_fields = ['status', 'notification_type']
    search_fields = ['message', 'medication__name']
    ordering_fields = ['created_at', 'status']
    permission_classes = [DoriPermission,]
    pagination_class = CustomPagination

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return NotificationListSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    """API endpoint for file attachments"""
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [DoriPermission,]
    parser_classes = (MultiPartParser, FormParser)

    # Limit to only GET and POST methods
    http_method_names = ['get', 'post']

class MedicationPrescriptionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MedicationPrescription.objects.all()
    serializer_class = MedicationPrescriptionSerializer
    permission_classes = [DoriPermission,]

class PrescribedMedicationListCreateView(ListAPIView):
    queryset = TavsiyaEtilganDori.objects.all()
    serializer_class = TavsiyaEtilganDoriModelSerializer
    permission_classes = [DoriPermission,]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MedicationTypeViewSet(viewsets.ModelViewSet):
#     queryset = MedicationType.objects.all()
#     serializer_class = MedicationTypeSerializer
#     permission_classes = []
#
#
# class MedicationViewSet(viewsets.ModelViewSet):
#     queryset = Medication.objects.all()
#     filter_backends = [filters.SearchFilter]
#     permission_classes = []
#     search_fields = ['name', 'type__name']
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return MedicationDetailSerializer
#         return MedicationSerializer
#
#     def get_queryset(self):
#         queryset = Medication.objects.all()
#
#         # Filter by medication type if provided
#         medication_type = self.request.query_params.get('type')
#         if medication_type:
#             queryset = queryset.filter(type__name__icontains=medication_type)
#
#         # Filter by name if provided
#         name = self.request.query_params.get('name')
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#
#         return queryset
#
#     @action(detail=True, methods=['post'])
#     def add_transaction(self, request, pk=None):
#         medication = self.get_object()
#
#         serializer = InventoryTransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(medication=medication)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(detail=True, methods=['get'])
#     def details(self, request, pk=None):
#         """Get detailed information about a medication for the info panel"""
#         medication = self.get_object()
#         try:
#             details = medication.details
#             serializer = MedicationDetailsSerializer(details)
#             return Response(serializer.data)
#         except MedicationDetails.DoesNotExist:
#             return Response({"detail": "No detailed information available"}, status=404)
#
#     @action(detail=False, methods=['get'])
#     def export_excel(self, request):
#         queryset = self.get_queryset()
#
#         # Create a DataFrame from the queryset
#         data = []
#         for medication in queryset:
#             data.append({
#                 'Dori turi': medication.type.name,
#                 'Dori nomi': medication.name,
#                 'Dori do\'zasi (mg)': f"{medication.dosage}",
#                 'Miqdori': medication.warehouse_quantity,
#                 'Kirim': medication.total_input,
#                 'Chiqim': medication.total_output,
#                 'Qoldiq': medication.balance
#             })
#
#         df = pd.DataFrame(data)
#
#         # Create an Excel file
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="kirimni_excelga_yuklab_olish.xlsx"'
#
#         # Write the DataFrame to the Excel file
#         df.to_excel(response, index=False)
#
#         return response
#
#
# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = Bemor.objects.all()
#     serializer_class = BemorSerializer
#     filter_backends = [filters.SearchFilter]
#     permission_classes = []
#     search_fields = ['first_name', 'last_name', 'patient_id']
#
#     @action(detail=True, methods=['get'])
#     def medications(self, request, pk=None):
#         """Get all medications assigned to a patient"""
#         patient = self.get_object()
#         transactions = patient.medication_transactions.all()
#
#         # Group by medication
#         medication_data = {}
#         for transaction in transactions:
#             med_id = transaction.medication.id
#             if med_id not in medication_data:
#                 medication_data[med_id] = {
#                     'medication': transaction.medication,
#                     'total_quantity': 0,
#                     'transactions': []
#                 }
#
#             medication_data[med_id]['transactions'].append(transaction)
#             if transaction.transaction_type == 'OUTPUT':
#                 medication_data[med_id]['total_quantity'] += transaction.quantity
#
#         # Serialize the data
#         result = []
#         for med_data in medication_data.values():
#             medication_serializer = MedicationSerializer(med_data['medication'])
#             transaction_serializer = InventoryTransactionSerializer(med_data['transactions'], many=True)
#
#             result.append({
#                 'medication': medication_serializer.data,
#                 'total_quantity': med_data['total_quantity'],
#                 'transactions': transaction_serializer.data
#             })
#
#         return Response(result)
#
#
# class InventoryTransactionViewSet(viewsets.ModelViewSet):
#     serializer_class = InventoryTransactionSerializer
#     filter_backends = [filters.SearchFilter]
#     permission_classes = []
#     search_fields = ['medication__name', 'medication__type__name', 'notes',
#                      'patient__first_name', 'patient__last_name']
#
#     def get_queryset(self):
#         queryset = InventoryTransaction.objects.all()
#
#         # Filter by archived status
#         archived = self.request.query_params.get('archived')
#         if archived == 'true':
#             queryset = queryset.filter(archived=True)
#         elif archived == 'false' or archived is None:
#             queryset = queryset.filter(archived=False)
#
#         # Filter by transaction type
#         transaction_type = self.request.query_params.get('type')
#         if transaction_type:
#             queryset = queryset.filter(transaction_type=transaction_type)
#
#         # Filter by date range
#         date_from = self.request.query_params.get('date_from')
#         if date_from:
#             try:
#                 date_from = make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
#                 queryset = queryset.filter(date__gte=date_from)
#             except ValueError:
#                 pass
#
#         date_to = self.request.query_params.get('date_to')
#         if date_to:
#             try:
#                 date_to = make_aware(datetime.strptime(date_to, '%Y-%m-%d'))
#                 queryset = queryset.filter(date__lte=date_to)
#             except ValueError:
#                 pass
#
#         # Filter by medication
#         medication_id = self.request.query_params.get('medication')
#         if medication_id:
#             queryset = queryset.filter(medication_id=medication_id)
#
#         # Filter by patient
#         patient_id = self.request.query_params.get('patient')
#         if patient_id:
#             queryset = queryset.filter(patient_id=patient_id)
#
#         return queryset
#
#     @action(detail=False, methods=['get'])
#     def archive_view(self, request):
#         """Special view for archived transactions with additional filtering"""
#         queryset = self.get_queryset().filter(archived=True)
#
#         # Group by date for display
#         date_grouped = {}
#         for transaction in queryset:
#             date_key = transaction.date.strftime('%d.%m.%Y')
#             if date_key not in date_grouped:
#                 date_grouped[date_key] = []
#             date_grouped[date_key].append(transaction)
#
#         # Convert to serialized data
#         result = {}
#         for date, transactions in date_grouped.items():
#             result[date] = InventoryTransactionSerializer(transactions, many=True).data
#
#         return Response(result)
#
#     @action(detail=False, methods=['get'])
#     def patient_archive_view(self, request):
#         """View for archived transactions grouped by"""
#
#
# class MedicationPrescriptionListCreateView(ListCreateAPIView):
#     queryset = MedicationPrescription.objects.all()
#     serializer_class = MedicationPrescriptionSerializer
#     permission_classes = []
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class MedicationPrescriptionDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = MedicationPrescription.objects.all()
#     serializer_class = MedicationPrescriptionSerializer
#     permission_classes = []
#
#

#
# class PrescribedMedicationDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = PrescribedMedication.objects.all()
#     serializer_class = PrescribedMedicationSerializer
#     permission_classes = []
#
# # Notifications
#
#
#
#
# class NotificationViewSet(viewsets.ModelViewSet):
#     """API endpoint for notifications"""
#     queryset = Notification.objects.all()
#     # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['status', 'notification_type']
#     search_fields = ['message', 'medication__name']
#     ordering_fields = ['created_at', 'status']
#     permission_classes = []
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return NotificationDetailSerializer
#         return NotificationListSerializer
#
#     @action(detail=True, methods=['post'])
#     def accept(self, request, pk=None):
#         """Accept a notification"""
#         notification = self.get_object()
#         notification.status = 'accepted'
#         notification.save()
#         return Response({'status': 'notification accepted'})
#
#     @action(detail=True, methods=['post'])
#     def reject(self, request, pk=None):
#         """Reject a notification"""
#         notification = self.get_object()
#         notification.status = 'rejected'
#         notification.save()
#         return Response({'status': 'notification rejected'})
#
#     @action(detail=True, methods=['get'])
#     def download_pdf(self, request, pk=None):
#         """Download notification as PDF"""
#         # You would implement PDF generation here
#         # For now, returning a placeholder response
#         return Response({'status': 'PDF download feature will be implemented'})
#
#     @action(detail=True, methods=['get'])
#     def attachments(self, request, pk=None):
#         """Get all attachments for a notification"""
#         notification = self.get_object()
#         attachments = notification.attachments.all()
#         serializer = AttachmentSerializer(attachments, many=True)
#         return Response(serializer.data)
#
#
# class AttachmentViewSet(viewsets.ModelViewSet):
#     """API endpoint for file attachments"""
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer
#     permission_classes = []
#
#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         """Download an attachment"""
#         attachment = self.get_object()
#         return FileResponse(attachment.file, as_attachment=True, filename=attachment.name)
#
#
