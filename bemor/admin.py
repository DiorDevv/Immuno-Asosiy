from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Manzil, OperatsiyaBolganJoy, BemorningHolati, Bemor, BemorQoshish, Viloyat, Tuman, Manzil, ArxivBemor


class BemorInline(admin.TabularInline):  # Bemorlarni boshqa adminlarda ichki jadval sifatida ko‘rsatish
    model = Bemor
    extra = 1
    autocomplete_fields = ['jinsi', 'manzil', 'bemor_holati']


@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)


@admin.register(Tuman)
class TumanAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'viloyat', 'tuman_tibbiyot_birlashmasi')
    search_fields = ('nomi', 'tuman_tibbiyot_birlashmasi')
    list_filter = ('viloyat',)


@admin.register(Manzil)
class ManzilAdmin(admin.ModelAdmin):
    list_display = ('mamlakat', 'viloyat', 'tuman', 'tuman_tibbiyot_birlashmasi', 'mahalla', 'kocha_nomi')
    search_fields = ('mahalla', 'kocha_nomi')
    list_filter = ('viloyat', 'tuman', 'tuman_tibbiyot_birlashmasi')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        """
        if db_field.name == "tuman":
            if "viloyat" in request.GET:
                kwargs["queryset"] = Tuman.objects.filter(viloyat_id=request.GET["viloyat"])
            else:
                kwargs["queryset"] = Tuman.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ("id", "JSHSHIR", "ism", "familiya", "tugilgan_sana", "jinsi")
    search_fields = ("JSHSHIR", "ism", "familiya")
    list_filter = ("jinsi", "tugilgan_sana")
    date_hierarchy = "tugilgan_sana"
    ordering = ("tugilgan_sana",)
    list_per_page = 20


@admin.register(ArxivBemor)
class ArxivBemorAdmin(admin.ModelAdmin):
    list_display = ("bemor", "qoshimcha_malumotlar")
    list_filter = ("bemor",)
    search_fields = ("bemor__ism", "bemor__familiya", "bemor__JSHSHIR")
    ordering = ("-qoshimcha_malumotlar",)
    readonly_fields = ("qoshimcha_malumotlar",)  # ❌ `updated_at` o‘chirildi
    autocomplete_fields = ("bemor", "bemor")  # ✅ TO‘G‘RI


@admin.register(Bemor)
class BemorAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', "bemor", "manzil", "bemor_holati", "operatsiya_bolgan_joy")
    search_fields = ("bemor__JSHSHIR", "bemor__ism", "bemor__familiya")
    list_filter = ("bemor__jinsi", "bemor_holati",)
    # date_hierarchy = "arxivga_olingan_sana"
    autocomplete_fields = ("bemor", "manzil", "bemor_holati", "operatsiya_bolgan_joy")
    # ordering = ("arxivga_olingan_sana",)
    list_per_page = 20
    fieldsets = (
        ("Bemor ma’lumotlari", {
            "fields": ("bemor",)
        }),
        ("Qo‘shimcha ma’lumotlar", {
            "fields": ("manzil", "bemor_holati", "operatsiya_bolgan_joy", "qoshimcha_malumotlar"),
            "classes": ("collapse",)
        }),
        # ("Arxiv", {
        #     "fields": ("arxivga_olingan_sana", "biriktirilgan_file"),
        #     "classes": ("collapse",)
        # }),
    )
    # readonly_fields = ("arxivga_olingan_sana",)

