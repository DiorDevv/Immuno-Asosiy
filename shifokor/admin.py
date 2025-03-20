from django.contrib import admin

from shifokor.models import ShifokorQoshish, Shifokorlar


class ShifokorInline(admin.TabularInline):  # Bemorlarni boshqa adminlarda ichki jadval sifatida ko‘rsatish
    model = ShifokorQoshish
    fields = '__all__'

@admin.register(Shifokorlar)
class ShifokorModeladmin(admin.ModelAdmin):
    shifokor = ShifokorInline
    list_display = ("shifokor", "lavozimi", "mutaxasislik_toifasi", "telefon_raqami", "biriktirilgan_muassasa",
                    "ish_staji", "oxirgi_malaka_oshirgan_joyi")


