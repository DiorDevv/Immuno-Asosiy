from django.db import models
from django.db.models import Model, CharField, IntegerField, DateField, TextField, ManyToManyField

from shared.models import BaseModel


class DoriTuri(Model):
    dori_dori = CharField(max_length=255)

    def __str__(self):
        return self.dori_dori

class Dori(BaseModel):
    nomi = CharField(max_length=255)
    dozasi = IntegerField()
    chiqarilgan_sana = DateField()
    yaroqlilik_muddati = DateField()
    fayl_turi = CharField(max_length=25)
    seria_raqam = CharField(max_length=25)

    def __str__(self):
        return self.nomi
class DoriQabulQilish(BaseModel):
    murojaat_sababi = TextField()
    berilgan_sana = DateField()
    davolash_turi = CharField(max_length=255)
    muassasa_nomi = CharField(max_length=255)

    def __str__(self):
        return self.berilgan_sana

class DoriQabulYakun(Model):
    qabul_qilish_sanasi = DateField()
    muddati = IntegerField()
    oxirgi_qabul_sanasi = DateField()
    bemor = ManyToManyField('bemor.Bemor', related_name='dori_qabul_yakun')

    def __str__(self):
        return self.bemor
