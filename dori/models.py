from django.db import models
from django.db.models import Model, CharField, IntegerField, DateField, TextField, ManyToManyField, PositiveIntegerField
from shared.models import BaseModel

class DoriTuri(Model):
    dori_dori = CharField(max_length=255)

    def __str__(self):
        return self.dori_dori

class Dori(BaseModel):
    nomi = CharField(max_length=255)
    dozasi = PositiveIntegerField()
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
        # Convert the date to a string
        return str(self.berilgan_sana)
        # Or provide more context, e.g.:
        # return f"{self.muassasa_nomi} - {self.berilgan_sana}"

class DoriQabulYakun(Model):
    qabul_qilish_sanasi = DateField()
    muddati = PositiveIntegerField(default=1)
    oxirgi_qabul_sanasi = DateField()
    bemor = ManyToManyField('bemor.Bemor', related_name='dori_qabul_yakun')

    def __str__(self):
        # Since bemor is a ManyToManyField, we can't return it directly
        # Instead, return something meaningful like the date or a combination
        return f"Qabul {self.qabul_qilish_sanasi}"
        # Or if you want to include bemor info:
        # return f"Qabul {self.qabul_qilish_sanasi} - {', '.join(bemor.str() for bemor in self.bemor.all())}"
