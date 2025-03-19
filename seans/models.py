from django.db.models import Model, FloatField, ForeignKey, CASCADE, DateField, CharField, BooleanField, FileField, \
    TextField, IntegerField


class AnalizNatijalar(Model):
    Gemoglabin = FloatField()
    Trombosit = FloatField()
    Leykosit = FloatField()
    Eritrosit = FloatField()
    Limfosit = FloatField()
    korik = ForeignKey('Korik', CASCADE, related_name='analiz_natijalari')




class Korik(Model):
    bemor = ForeignKey('bemor.Bemor', CASCADE, related_name='seanslar')
    korik_otkazilgan_sana = DateField(auto_now=True)
    murojat_turi = CharField(max_length=255)
    qon_olingan_sana = DateField(auto_now=True)
    qon_analiz_qilingan_sana = DateField(auto_now=True)
    reagent_ishlatildi = BooleanField(db_default=False)
    shifokor = ForeignKey('shifokor.Shifokorlar', CASCADE, related_name='koriklar')
    biriktirilgan_fayllar = FileField()
    description = TextField()

class TavsiyaQilinganDorilar(Model):
    dori = ForeignKey('dori.MedicationType', CASCADE)
    korik = ForeignKey('Korik', CASCADE)
    dozasi = IntegerField()


