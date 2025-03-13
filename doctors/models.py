from django.db import models

class Shifokor(Model):
    JSHSHIR = BigIntegerField()

class ShaxsiyMalumot(Model):
    ism = CharField(max_length=255)
    familiya = CharField(max_length=255)
    tasdiqlangan = CharField(max_length=255)
    tugilgan_sana = DateField()
    lavozim = CharField(max_length=255)
    telefon_raqam = BigIntegerField()
    ish_joyi = CharField(max_length=255)
    oldingi_malaka_oshirish = CharField(max_length=255)
    qayta_malaka_oshirish = CharField(max_length=255)
    operatsiya_vaqti = DateField()
    biriktirilgan_tibbiy = CharField(max_length=255)
    jinsi = ForeignKey(Jinsi, CASCADE, related_name='shaxsiymalumotlar')
    oxirgi_ozgartirilgan_vaqt = DateTimeField()
    arxivga_olingan_sana = DateTimeField()
