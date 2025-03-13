from rest_framework.serializers import ModelSerializer

from shifokor.models import Shifokorlar, Shifokor_qoshish
from rest_framework.serializers import ValidationError

class ShifokorModelSerializer(ModelSerializer):
    class Meta:
        model = Shifokorlar
        fields = '__all__'



class Shifokor_qoshishModelSerializer(ModelSerializer):
    class Meta:
        model = Shifokor_qoshish
        fields = ['jshshir',]


    def validate_JSHSHIR(self, value):
        if not value.isdigit() or len(value) != 14:
            raise ValidationError("JSHSHIR faqat 14 ta raqamdan iborat bo‘lishi kerak!")

        return value

    def validate(self, attrs):
        JSHSHIR = attrs.get("JSHSHIR")

        shifokor = Shifokor_qoshish.objects.filter(JSHSHIR=JSHSHIR).first()
        if shifokor:
            return {
                "JSHSHIR": shifokor.JSHSHIR
            }

        raise ValidationError(
            "Bunday jshshirga ega shifokor mavjud emas"
        )

