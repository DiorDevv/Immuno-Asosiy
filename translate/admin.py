from django.contrib import admin

from .models import Translate, Languege

@admin.register(Translate)
class TranslateAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'lang')
    list_filter = ('lang__name',)
    search_fields = ('key', 'value')


@admin.register(Languege)
class LanguegeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

