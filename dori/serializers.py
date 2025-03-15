# serializers.py
from rest_framework import serializers
from bemor.models import Bemor  # Assuming this exists
from dori.models import Dori, DoriQabulQilish, DoriQabulYakun, DoriTuri


# First, let's create a serializer for DoriTuri
class DoriTuriSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoriTuri
        fields = ['id', 'dori_dori']


# Serializer for Dori (Medicine)
class MedicineSerializer(serializers.ModelSerializer):
    # Adding DoriTuri as a nested serializer if there's a relationship
    dori_turi = DoriTuriSerializer(read_only=True, required=False)

    class Meta:
        model = Dori
        fields = [
            'id',
            'nomi',
            'dozasi',
            'chiqarilgan_sana',
            'yaroqlilik_muddati',
            'fayl_turi',
            'seria_raqam',
            'dori_turi',  # Assuming a relationship might exist
            'created_at',  # From BaseModel
            'updated_at',  # From BaseModel
        ]
        read_only_fields = ['created_at', 'updated_at']


# Serializer for DoriQabulQilish
class DoriQabulQilishSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoriQabulQilish
        fields = [
            'id',
            'murojaat_sababi',
            'berilgan_sana',
            'davolash_turi',
            'muassasa_nomi',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# Serializer for DoriQabulYakun
class DoriQabulYakunSerializer(serializers.ModelSerializer):
    # Adding bemor as a nested relationship
    bemor = serializers.PrimaryKeyRelatedField(
        queryset=Bemor.objects.all(),
        many=True
    )

    class Meta:
        model = DoriQabulYakun
        fields = [
            'id',
            'qabul_qilish_sanasi',
            'muddati',
            'oxirgi_qabul_sanasi',
            'bemor',
        ]


# Assuming a Bemor model exists, here's a serializer for it
class PatientSerializer(serializers.ModelSerializer):
    # Nested relationships
    medicines = MedicineSerializer(many=True, read_only=True)
    dori_qabul_yakun = DoriQabulYakunSerializer(many=True, read_only=True)

    class Meta:
        # Assuming these fields exist in Bemor model
        model = Bemor
        fields = [
            'id',
            'medicines',  # Assuming ManyToMany with Dori
            'dori_qabul_yakun',  # From the ManyToMany in DoriQabulYakun
            # Add other Bemor fields here as needed
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Custom create method if needed
        return Bemor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Custom update method if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance