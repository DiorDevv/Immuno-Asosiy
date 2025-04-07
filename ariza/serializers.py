from rest_framework import serializers

from dori.models import MedicationType
from .models import *

class TransplantCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransplantCenter
        fields = '__all__'


class ToWhomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToWhom
        fields = '__all__'


# class ApplicationStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ApplicationStatus
#         fields = '__all__'


class MedicationTypeAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationType
        fields = '__all__'


class MedicationAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationApp
        fields = '__all__'


class ApplicationMedicationSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)

    class Meta:
        model = ApplicationMedication
        fields = ['id', 'medication', 'medication_name', 'dosage', 'quantity', 'days_scheduled']


class ApplicationListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    # from_center_name = serializers.CharField(source='from_center.name', read_only=True)
    to_center_name = serializers.CharField(source='to_center.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'director_name', 'to_center',
                  'to_center_name', 'position', 'position_name', 'date', 'status', 'status_name']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    medications = ApplicationMedicationSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    to_center_name = serializers.CharField(source='to_center.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    medications = ApplicationMedicationSerializer(many=True, required=False)

    class Meta:
        model = Application
        fields = ['director_name', 'to_center', 'position', 'date',
                  'status', 'patient_count',
                  'medications']

    def create(self, validated_data):
        medications_data = validated_data.pop('medications', [])
        application = Application.objects.create(**validated_data)


        for medication_data in medications_data:
            ApplicationMedication.objects.create(application=application, **medication_data)

        return application

    def update(self, instance, validated_data):
        medications_data = validated_data.pop('medications', [])

        # Update the application instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle medications
        existing_medications = {med.id: med for med in instance.medications.all()}

        # Update or create medications
        for medication_data in medications_data:
            medication_id = medication_data.get('id')
            if medication_id and medication_id in existing_medications:
                # Update existing medication
                med = existing_medications.pop(medication_id)
                for attr, value in medication_data.items():
                    setattr(med, attr, value)
                med.save()
            else:
                # Create new medication
                ApplicationMedication.objects.create(application=instance, **medication_data)

        # Delete any remaining medications that weren't in the update data
        for med in existing_medications.values():
            med.delete()

        return instance