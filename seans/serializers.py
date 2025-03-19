from rest_framework.serializers import ModelSerializer
from models import AnalizNatijalar, TavsiyaQilinganDorilar, Korik
from dori.serializers import MedicationTypeSerializer


class AnalizNatijalarModelSerializer(ModelSerializer):
    class Meta:
        model = AnalizNatijalar
        fields = "__all__"


class TavsiyaQilinganDorilarModelSerializer(ModelSerializer):
    class Meta:
        model = TavsiyaQilinganDorilar
        fields = 'dori', 'dozasi'


class KorikModelSerializer(ModelSerializer):
    dori = MedicationTypeSerializer(many=True)
    tavsiya_qilingan_dorilar = TavsiyaQilinganDorilarModelSerializer(source='korik_dori_set', many=True, read_only=True)
    analiz_natijalari = AnalizNatijalarModelSerializer()

    class Meta:
        model = Korik
        fields = ("bemor", "korik_otkazilgan_sana", "murojat_turi", "qon_olingan_sana", "qon_analiz_qilingan_sana",
                  "reagent_ishlatildi", "shifokor", "biriktirilgan_fayllar", "description")
