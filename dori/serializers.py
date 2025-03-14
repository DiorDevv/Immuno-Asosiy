from rest_framework.serializers import ModelSerializer

from bemor.models import Bemor
from dori.models import Dori, DoriQabulQilish


class MedicineSerializer(ModelSerializer):
    class Meta:
        model = Dori
        fields = "__all__"

class PatientSerializer(ModelSerializer):
    medicines = MedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Bemor
        fields = "__all__"

class DoriQAbulYakunModelSerializer(ModelSerializer):
    class Meta:
        model = DoriQabulQilish
        fields = '__all__'