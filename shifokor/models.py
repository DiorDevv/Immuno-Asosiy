from django.db.models import Model
from rest_framework.fields import CharField, DateField, IntegerField

class Shifokorlar(Model):
    fio = CharField(max_length=150)
    tugilgan_sana = DateField(allow_null=False)
    lavozimi = CharField(max_length=100)
    mutaxasislik_toifasi = CharField(max_length=100)
    telefon_raqami = CharField(max_length=13)
    biriktirilgan_muassasa = CharField(allow_null=True)
    jshshir = IntegerField(max_value=99999999999999)
    ish_staji = IntegerField()
    oxirgi_malaka_oshirgan_joyi = CharField(max_length=150)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        a = self.user.name
        obj = self.object
        obj.mutaxasislik_toifasi = a
        obj.save(self, *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,)

