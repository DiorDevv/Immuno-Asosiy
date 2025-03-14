from django.db import models
from django.db.models import Model, CharField, IntegerField, DateField, TextField, ManyToManyField


class DoriTuri(Model):
    dori_dori = CharField(max_length=255)

class Dori(Model):
    nomi = CharField(max_length=255)
    dozasi = IntegerField()
    chiqarilgan_sana = DateField()
    yaroqlilik_muddati = DateField()
    fayl_turi = CharField(max_length=25)
    seria_raqam = CharField(max_length=25)

class DoriQabulQilish(Model):
    murojaat_sababi = TextField()
    berilgan_sana = DateField()
    davolash_turi = CharField(max_length=255)
    muassasa_nomi = CharField(max_length=255)

class DoriQabulYakun(Model):
    qabul_qilish_sanasi = DateField()
    muddati = IntegerField()
    oxirgi_qabul_sanasi = DateField()
    bemor = ManyToManyField('Bemor', related_name='dori_qabul_yakun')
