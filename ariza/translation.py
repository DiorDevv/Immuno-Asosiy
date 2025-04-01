from modeltranslation.translator import register, TranslationOptions
from .models import TransplantCenter, ToWhom, ApplicationStatus, MedicationTypeApp, MedicationApp, Application, \
    ApplicationMedication


@register(TransplantCenter)
class ArizaTranslation(TranslationOptions):
    fields = ('name',)

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