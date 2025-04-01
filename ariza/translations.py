from modeltranslation.translator import Translator

from modeltranslation.translator import register, TranslationOptions
from ariza.models import TransplantCenter, ToWhom, ApplicationStatus, MedicationTypeApp, MedicationApp, Application, \
    ApplicationMedication
from dori.models import MedicationType


@register(TransplantCenter)
class ArizaTranslation(TranslationOptions):
    fields = ['name', ]

@register(ToWhom)
class ToWhomTranslation(TranslationOptions):
    fields = ['name']

@register(ApplicationStatus)
class ApplicationStatusTranslation(TranslationOptions):
    fields = ['type']

@register(MedicationTypeApp)
class MedicationTypeAppTranslation(TranslationOptions):
    fields = ['name']

@register(MedicationApp)
class MedicationAppTranslation(TranslationOptions):
    fields = ['name']

@register(Application)
class ApplicationTranslation(TranslationOptions):
    fields = ['director_name', 'position']

@register(ApplicationMedication)
class ApplicationMedicationTranslation(TranslationOptions):
    fields = ['dosage']