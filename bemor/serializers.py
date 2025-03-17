from rest_framework import serializers
from .models import BemorQoshish, Manzil, OperatsiyaBolganJoy, BemorningHolati, Bemor, Viloyat, Tuman
import re
from django.utils import timezone
import os


class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viloyat
        fields = "__all__"


class TumanSerializer(serializers.ModelSerializer):
    viloyat_nomi = serializers.CharField(source="viloyat.nomi", read_only=True)

    class Meta:
        model = Tuman
        fields = ["id", "nomi", "viloyat", "viloyat_nomi", "tuman_tibbiyot_birlashmasi"]


class BemorQoshishSerializer(serializers.ModelSerializer):
    class Meta:
        model = BemorQoshish
        fields = ['JSHSHIR', 'ism', 'familiya', 'tugilgan_sana', 'jinsi']

    def validate_JSHSHIR(self, value):
        if not value.isdigit() or len(value) != 14:
            raise serializers.ValidationError("JSHSHIR faqat 14 ta raqamdan iborat bo‘lishi kerak!")

        return value

    def validate(self, attrs):
        JSHSHIR = attrs.get("JSHSHIR")
        ism = attrs.get("ism")
        familiya = attrs.get("familiya")
        tugilgan_sana = attrs.get("tugilgan_sana")

        bemor = BemorQoshish.objects.filter(JSHSHIR=JSHSHIR).first()
        if bemor:
            return {
                "JSHSHIR": bemor.JSHSHIR,
                "ism": bemor.ism,
                "familiya": bemor.familiya,
                "tugilgan_sana": bemor.tugilgan_sana,
                "jinsi": bemor.jinsi,
            }

        if BemorQoshish.objects.filter(ism=ism, familiya=familiya, tugilgan_sana=tugilgan_sana).exists():
            raise serializers.ValidationError(
                {"detail": "Bunday ism, familiya va tug‘ilgan sanaga ega bemor allaqachon mavjud!"}
            )

        return attrs


class ManzilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manzil
        fields = "__all__"

    def validate_mamlakat(self, value):
        ruxsat_berilgan_davlatlar = ["O'zbekiston", "Rossiya", "AQSh", "Qozog'iston", "Turkiya"]
        if value not in ruxsat_berilgan_davlatlar:
            raise serializers.ValidationError("Bu davlatga ruxsat berilmagan.")
        return value

    def validate_hudud(self, value):
        if not re.match(r"^[a-zA-Z\s'-]+$", value):
            raise serializers.ValidationError("Hudud faqat harflardan iborat bo‘lishi kerak.")
        return value

    def validate_kocha_nomi(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Ko'cha nomi kamida 3 ta belgidan iborat bo‘lishi kerak.")
        return value

    def validate_biriktirilgan_tuman(self, value):
        if not value.strip():
            raise serializers.ValidationError("Biriktirilgan tuman maydoni bo‘sh bo‘lishi mumkin emas.")
        return value


class OperatsiyaBolganJoySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatsiyaBolganJoy
        fields = '__all__'

class BemorningHolatiSerializer(serializers.ModelSerializer):
    class Meta:
        model = BemorningHolati
        fields = '__all__'


class BemorSerializer(serializers.ModelSerializer):
    """ Bemor obyektlari uchun serializer """
    bemor = BemorQoshishSerializer()  # ID o‘rniga to‘liq obyekt
    manzil = ManzilSerializer()
    bemor_holati = BemorningHolatiSerializer()
    operatsiya_bolgan_joy = OperatsiyaBolganJoySerializer()

    class Meta:
        model = Bemor
        fields = '__all__'  # Hammasini olish

    def validate_arxivga_olingan_sana(self, value):
        """ Arxivga olingan sana validatsiyasi """
        if value and value > timezone.now():
            raise serializers.ValidationError("Arxivga olish sanasi kelajakdagi sana bo‘lishi mumkin emas!")
        if value and self.instance and value < self.instance.created_at:
            raise serializers.ValidationError(
                "Arxivga olish sanasi bemor yaratilgan sanadan oldin bo‘lishi mumkin emas!")
        return value

    def validate_biriktirilgan_file(self, value):
        """ Fayl formatini tekshirish """
        if value:
            ext = os.path.splitext(value.name)[1].lower()
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            max_size = 5 * 1024 * 1024  # 5MB gacha ruxsat
            if ext not in allowed_extensions:
                raise serializers.ValidationError("Faqat PDF yoki JPG formatdagi fayllarga ruxsat berilgan!")
            if value.size > max_size:
                raise serializers.ValidationError("Fayl hajmi 5MB dan oshib ketdi!")
        return value

    def validate(self, data):
        errors = {}

        if not data.get('bemor'):
            errors['bemor'] = "Bemor maydoni bo‘sh bo‘lishi mumkin emas!"

        if not data.get('bemor_holati'):
            errors['bemor_holati'] = "Bemor holati tanlanishi shart!"

        if errors:
            raise serializers.ValidationError(errors)

        return data
