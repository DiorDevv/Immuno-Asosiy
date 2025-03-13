from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Manzil, OperatsiyaBolganJoy, BemorningHolati, Bemor, BemorQoshish
from django.utils.translation import gettext_lazy as _

class BemorInline(admin.TabularInline):  # Bemorlarni boshqa adminlarda ichki jadval sifatida ko‘rsatish
    model = Bemor
    extra = 1
    autocomplete_fields = ['jinsi', 'manzil', 'bemor_holati']


@admin.register(Manzil)
class ManzilAdmin(ExportMixin, admin.ModelAdmin):  # Export funksiyasi qo‘shildi
    list_display = ('mamlakat', 'hudud', 'tuman', 'mahalla', 'kocha_nomi', 'biriktirilgan_tuman')
    search_fields = ('mamlakat', 'hudud', 'tuman', 'mahalla')
    list_filter = ('mamlakat', 'hudud', 'tuman')
    ordering = ('mamlakat', 'hudud', 'tuman')
    list_per_page = 20


@admin.register(OperatsiyaBolganJoy)
class OperatsiyaBolganJoyAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'mamlakat', 'operatsiya_bolgan_joy', 'transplantatsiya_sana', 'operatsiya_oxirlangan_sana',
        'ishlatilgan_miqdor')
    search_fields = ('mamlakat', 'operatsiya_bolgan_joy')
    list_filter = ('mamlakat', 'transplantatsiya_sana')
    ordering = ('transplantatsiya_sana',)
    date_hierarchy = 'transplantatsiya_sana'
    list_per_page = 20


@admin.register(BemorningHolati)
class BemorningHolatiAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('holati', 'ozgarish')
    search_fields = ('holati',)
    ordering = ('holati',)
    list_per_page = 20


@admin.register(BemorQoshish)
class BemorQoshsihAdmin(admin.ModelAdmin):
    list_display = ("id","JSHSHIR", "ism", "familiya", "tugilgan_sana", "jinsi")
    search_fields = ("JSHSHIR", "ism", "familiya")
    list_filter = ("jinsi", "tugilgan_sana")
    date_hierarchy = "tugilgan_sana"
    ordering = ("tugilgan_sana",)
    list_per_page = 20


@admin.register(Bemor)
class BemorAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("bemor", "manzil", "bemor_holati", "operatsiya_bolgan_joy", "arxivga_olingan_sana")
    search_fields = ("bemor__JSHSHIR", "bemor__ism", "bemor__familiya")
    list_filter = ("bemor__jinsi", "bemor_holati", "arxivga_olingan_sana")
    date_hierarchy = "arxivga_olingan_sana"
    autocomplete_fields = ("bemor", "manzil", "bemor_holati", "operatsiya_bolgan_joy")
    ordering = ("arxivga_olingan_sana",)
    list_per_page = 20
    fieldsets = (
        ("Bemor ma’lumotlari", {
            "fields": ("bemor",)
        }),
        ("Qo‘shimcha ma’lumotlar", {
            "fields": ("manzil", "bemor_holati", "operatsiya_bolgan_joy", "qoshimcha_malumotlar"),
            "classes": ("collapse",)
        }),
        ("Arxiv", {
            "fields": ("arxivga_olingan_sana", "biriktirilgan_file"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("arxivga_olingan_sana",)
