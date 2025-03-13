from shifokor.models import Shifokorlar, Shifokor_qoshish
from django.contrib import admin

@admin.register(Shifokorlar)
class ShifokorAdmin(admin.ModelAdmin):
    list_display = ('shifokor', 'lavozimi', 'mutaxasislik_toifasi', 'telefon_raqami', 'biriktirilgan_muassasa', 'ish_staji', 'oxirgi_malaka_oshirgan_joyi')
    plural_name = 'Shifokorlar'


@admin.register(Shifokor_qoshish)
class Shifokor_qoshish(admin.ModelAdmin):
    list_display = ('jshshir', 'ismi', 'familya', 'otasining_ismi', 'tugilgan_sana')









