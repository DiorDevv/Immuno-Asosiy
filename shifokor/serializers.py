from rest_framework.serializers import ModelSerializer, CharField

from shifokor.models import Shifokorlar, ShifokorQoshish
from rest_framework.serializers import ValidationError

class ShifokorModelSerializer(ModelSerializer):
    class Meta:
        model = Shifokorlar
        fields = ("shifokor","lavozimi","mutaxasislik_toifasi","telefon_raqami",
                   "ish_staji", "oxirgi_malaka_oshirgan_joyi", 'biriktirilgan_muassasa')




class ShifokorQoshishModelSerializer(ModelSerializer):
    class Meta:
        model = ShifokorQoshish
        fields = ['jshshir',]



    def validate_jshshir(self, value):
        if not value.isdigit() or len(value) != 14:
            raise ValidationError("JSHSHIR faqat 14 ta raqamdan iborat bo‘lishi kerak!")

        return value

    def validate(self, attrs):
        jshshir = attrs.get("jshshir")

        shifokor = ShifokorQoshish.objects.filter(jshshir=jshshir).first()
        if shifokor:
            return {
                "jshshir": shifokor.jshshir
            }

        raise ValidationError(
            "Bunday jshshirga ega shifokor mavjud emas"
        )

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)




class ShifokorListSerializer(ModelSerializer):
    ismi = CharField(source='shifokor__ismi', read_only=True)
    familya = CharField(source='shifokor__familya', read_only=True)
    otasining_ismi = CharField(source='shifokor__otasining_ismi', read_only=True)
    tugilgan_sana = CharField(source='shifokor__tugilgan_sana', read_only=True)
    class Meta:
        model = Shifokorlar
        fields = ('id', 'ismi', 'familya', 'otasining_ismi', 'tugilgan_sana', 'lavozimi', 'mutaxasislik_toifasi',
                  'telefon_raqami')
        print(fields.__class__)















