from modeltranslation.translator import register, TranslationOptions, translator

from .models import Viloyat, Tuman


# 1-usul
@register(Viloyat)
class ViloyatTranslationOptions(TranslationOptions):
    fields = ('nomi',)

@register(Tuman)
class TumanTranslationOptions(TranslationOptions):
    fields = ('nomi', 'tuman_tibbiyot_birlashmasi')

# # 2-usul
# translator.register(Tuman, ViloyatTranslationOptions)
