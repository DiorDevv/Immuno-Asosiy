from django.db.models import Sum
from rest_framework import serializers
from .models import MedicationType, Medication, InventoryTransaction, Bemor, MedicationDetails, TavsiyaEtilganDori, \
    MedicationPrescription
from rest_framework import serializers
from .models import QabulQilishYakuniy

class MedicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationType
        fields = ['id', 'name']


class MedicationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDetails
        fields = ['id', 'description', 'usage_instructions', 'side_effects',
                  'contraindications', 'storage_instructions']




class InventoryTransactionSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    medication_type = serializers.CharField(source='medication.type.name', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = InventoryTransaction
        fields = ['id', 'medication', 'medication_name', 'medication_type',
                  'transaction_type', 'transaction_type_display',
                  'quantity', 'date', 'notes', 'archived',
                  'patient', 'patient_name']


class MedicationSerializer(serializers.ModelSerializer):
    total_input = serializers.IntegerField(read_only=True)
    total_output = serializers.IntegerField(read_only=True)
    balance = serializers.IntegerField(read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    details = MedicationDetailsSerializer(read_only=True)

    class Meta:
        model = Medication
        fields = ['id', 'name', 'type', 'type_name', 'dosage', 'dosage_unit',
                  'total_input', 'total_output', 'balance', 'warehouse_quantity',
                  'details']


class MedicationDetailSerializer(MedicationSerializer):
    inventory_transactions = InventoryTransactionSerializer(many=True, read_only=True)

    class Meta(MedicationSerializer.Meta):
        fields = MedicationSerializer.Meta.fields + ['inventory_transactions']

class MedicationSerializer(serializers.ModelSerializer):
    # total_input=serializers.SerializerMethodField()
    # total_output=serializers.SerializerMethodField()
    # balance=serializers.SerializerMethodField()
    class Meta:
        model = Medication
        # fields = ['id', 'name', 'dosage_unit', "total_input", "total_output", "balance"]
        fields = ['id', 'name', 'dosage_unit', "total_input", "total_output", "balance", "warehouse_quantity"]
        # Adjust fields based on your Medication model

    # def get_total_input(self, obj):
    #     return InventoryTransaction.objects.filter(transaction_type="INPUT", medication=obj).aggregate(Sum("quantity"))["quantity__sum"]
    #
    # def get_total_output(self, obj):
    #     return InventoryTransaction.objects.filter(transaction_type="OUTPUT", medication=obj).aggregate(Sum("quantity"))["quantity__sum"]
    #
    # def get_balance(self, obj):
    #     return obj.total_input-obj.total_output


class TavsiyaEtilganDoriSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(read_only=True)  # Nested serializer for medication details
    medication_id = serializers.PrimaryKeyRelatedField(
        queryset=Medication.objects.all(),
        write_only=True,
        source='medication'
    )

    class Meta:
        model = TavsiyaEtilganDori
        fields = [
            'id','medication_id','medication', 'bemor', 'dori_nomi', 'kunlik_doza',
            'miqdori', 'seria_raqam', 'yaroqlilik_muddati', 'boshlanish',
            'tugallanish', 'qabul_qilish_muddati', 'is_active'
        ]
        read_only_fields = ['is_active']  # Calculated property

class MedicationPrescriptionSerializer(serializers.ModelSerializer):
    medications = TavsiyaEtilganDoriSerializer(many=True, read_only=True)  # Nested medications
    patient = serializers.StringRelatedField()  # Display patient full_name

    class Meta:
        model = MedicationPrescription
        fields = [
            'id', 'patient', 'prescription_date', 'prescription_number',
            'institution', 'doctor', 'reason', 'is_active', 'medications'
        ]
        read_only_fields = ['medications']  # Medications are managed separately

    def create(self, validated_data):
        # Handle creation of prescription and link to patient
        medications_data = self.context.get('request').data.get('medications', [])
        prescription = MedicationPrescription.objects.create(**validated_data)
        for med_data in medications_data:
            TavsiyaEtilganDori.objects.create(prescription=prescription, **med_data)
        return prescription

    def update(self, instance, validated_data):
        # Update prescription details
        instance.prescription_date = validated_data.get('prescription_date', instance.prescription_date)
        instance.prescription_number = validated_data.get('prescription_number', instance.prescription_number)
        instance.institution = validated_data.get('institution', instance.institution)
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance



class QabulQilishYakuniySerializer(serializers.ModelSerializer):
    class Meta:
        model = QabulQilishYakuniy
        fields = [
            'id',
            'preparatni_qabul_qilish_sanasi',
            'preparatni_qabul_qilish_muddati',
            'oxirgi_qabul_qilish_sanasi'
        ]
        read_only_fields = ['oxirgi_qabul_qilish_sanasi']

# Notifications

from rest_framework import serializers
from .models import Medication, Notification, Attachment


# class MedicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Medication
#         fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'name', 'uploaded_at']


class NotificationListSerializer(serializers.ModelSerializer):
    """Serializer for listing notifications (Image 1)"""
    sana = serializers.DateTimeField(source='created_at', format='%d.%m.%Y', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'quantity', 'sana', 'status', 'status_display']


class NotificationDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed notification view (Image 2)"""
    sana = serializers.DateTimeField(source='created_at', format='%d.%m.%Y', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # Medication details
    bemor = serializers.CharField(source='medication.get_type_display', read_only=True)
    dori_nomi = serializers.CharField(source='medication.name', read_only=True)
    dori_dozasi = serializers.FloatField(source='medication.dosage', read_only=True)
    miqdori = serializers.IntegerField(source='medication.quantity', read_only=True)
    seriya_raqami = serializers.CharField(source='medication.serial_number', read_only=True)
    ishlab_chiqarilgan_sana = serializers.DateField(
        source='medication.production_date',
        format='%d.%m.%Y',
        read_only=True
    )
    yaroqlilik_muddati = serializers.DateField(
        source='medication.expiry_date',
        format='%d.%m.%Y',
        read_only=True
    )

    # Attachment info
    has_attachments = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'sana', 'status', 'status_display',
            'bemor', 'dori_nomi', 'dori_dozasi', 'miqdori',
            'seriya_raqami', 'ishlab_chiqarilgan_sana', 'yaroqlilik_muddati',
            'has_attachments'
        ]

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

