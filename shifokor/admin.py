from django.contrib import admin

from shifokor.models import ShifokorQoshish, Shifokorlar

@admin.register(ShifokorQoshish)
class ShifokorQoshishModelAdmin(admin.ModelAdmin):  # Bemorlarni boshqa adminlarda ichki jadval sifatida ko‘rsatish
    model = ShifokorQoshish
    fields = ("jshshir", "familya", "ismi", "otasining_ismi", "jinsi", "tugilgan_sana")

@admin.register(Shifokorlar)
class ShifokorModeladmin(admin.ModelAdmin):
    shifokor = ShifokorQoshishModelAdmin
    list_display = ("shifokor", "lavozimi", "mutaxasislik_toifasi", "telefon_raqami", "biriktirilgan_muassasa",
                    "ish_staji", "oxirgi_malaka_oshirgan_joyi")


