from rest_framework.fields import CharField, ListField, FloatField
from rest_framework.serializers import ModelSerializer
from .models import AnalizNatijalar, TavsiyaQilinganDorilar, Korik
from dori.serializers import MedicationTypeSerializer, MedicationSerializer
from bemor.models import Bemor

class TavsiyaQilinganDorilarModelSerializer(ModelSerializer):
    dori_turi = CharField(source='dori.name', read_only=True)
    class Meta:
        model = TavsiyaQilinganDorilar
        fields = 'dozasi', 'dori_turi'


class BemorSeansModelSerializer(ModelSerializer):
    ism = CharField(source='bemor.ism')
    familya = CharField(source='bemor.familiya')
    tugilgan_sana = CharField(source='bemor.tugilgan_sana')
    class Meta:
        model = Bemor
        fields = ('id', "ism", "familya", "tugilgan_sana")


class AnalizNatijalarModelSerializer(ModelSerializer):
    class Meta:
        model = AnalizNatijalar
        fields = ("gemoglabin","trombosit","leykosit","eritrosit","limfosit","korik")


class KorikModelSerializer(ModelSerializer):
    bemor = BemorSeansModelSerializer()
    # dori = MedicationTypeSerializer(many=True)
    tavsiya_qilingan_dorilar = TavsiyaQilinganDorilarModelSerializer(source='korik_dorilari', many=True)
    analiz_natijalari = AnalizNatijalarModelSerializer(many=True, read_only=True)

    class Meta:
        model = Korik
        fields = ("bemor", "korik_otkazilgan_sana", "murojat_turi", "qon_olingan_sana", "qon_analiz_qilingan_sana",
                  "reagent_ishlatildi", "shifokor", "biriktirilgan_fayllar", "description", 'tavsiya_qilingan_dorilar',
                  'analiz_natijalari')

