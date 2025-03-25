from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from .models import AnalizNatijalar, TavsiyaQilinganDorilar, Korik
from dori.serializers import MedicationTypeSerializer
from bemor.models import Bemor

class AnalizNatijalarModelSerializer(ModelSerializer):
    class Meta:
        model = AnalizNatijalar
        fields = "__all__"


class TavsiyaQilinganDorilarModelSerializer(ModelSerializer):
    class Meta:
        model = TavsiyaQilinganDorilar
        fields = 'dori', 'dozasi'


class BemorSeansModelSerializer(ModelSerializer):
    ism = CharField(source='bemor.ism')
    familya = CharField(source='bemor.familiya')
    tugilgan_sana = CharField(source='bemor.tugilgan_sana')
    class Meta:
        model = Bemor
        fields = ('id', "ism", "familya", "tugilgan_sana")



class KorikModelSerializer(ModelSerializer):
    bemor = BemorSeansModelSerializer()
    dori = MedicationTypeSerializer(many=True)
    tavsiya_qilingan_dorilar = TavsiyaQilinganDorilarModelSerializer(source='korik_dori_set', many=True)
    analiz_natijalari = AnalizNatijalarModelSerializer()

    class Meta:
        model = Korik
        fields = ("bemor", "korik_otkazilgan_sana", "murojat_turi", "qon_olingan_sana", "qon_analiz_qilingan_sana",
                  "reagent_ishlatildi", "shifokor", "biriktirilgan_fayllar", "description", 'tavsiya_qilingan_dorilar',
                  'dori', 'analiz_natijalari')
