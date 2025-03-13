from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE, BigIntegerField, SmallIntegerField, \
    DateField, FileField, DateTimeField, TextChoices, TextField

from bemor.models import Bemor


class DoriTuri(Model):
    dori_turi = CharField(max_length=255)

class Dori(Model):
    nomi = CharField(max_length=255)
    dori_turi = ForeignKey(DoriTuri, on_delete=CASCADE, related_name='dorilar')
    ishlab_chiqarilgan_sana = DateField()
    yaroqlilik_muddat = DateField()
    davlat = CharField(max_length=255)
    seriya_raqami = CharField(max_length=255)

class DoriQabul(Model):
    boshlangan_sana = DateField()
    davomiyligi = IntegerField()
    tugash_sanasi = DateField()

class Kirim(Model):
    dori = ForeignKey(Dori, on_delete=CASCADE, related_name='kirimlar')
    miqdor = BigIntegerField()
    kirim_vaqti = DateTimeField()
    jami = BigIntegerField()

class Chiqim(Model):
    sabab = TextField()
    dori_berilgan_sana = DateTimeField()
    davolash_turi = CharField(max_length=255)
    muassasa_nomi = CharField(max_length=255)
    bemor_hadjas = ForeignKey(Bemor, on_delete=CASCADE, related_name='chiqimlar')
    tavsiya_qilingan_dori = ForeignKey(Dori, on_delete=CASCADE)
    dori_qabul_qilingan_hadjas = ForeignKey(DoriQabul, on_delete=CASCADE)
    davomiyligi = BigIntegerField()
    lsanasi = DateField()
    davomiylik = ForeignKey(DoriQabul, on_delete=CASCADE, related_name='chiqimlar')

class ArxivD(Model):
    chiqim = ForeignKey(Chiqim, on_delete=CASCADE)
    kirim = ForeignKey(Kirim, on_delete=CASCADE)

