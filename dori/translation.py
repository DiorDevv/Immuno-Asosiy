from modeltranslation.translator import register, TranslationOptions

from dori.models import MedicationType, MedicationDetails, MedicationPrescription, TavsiyaEtilganDori, Medication


@register(MedicationType)
class MedicationTypeTranslation(TranslationOptions):
    fields = ('name',)

@register(Medication)
class MedicationTranslation(TranslationOptions):
    fields = ('name', 'dosage_unit')

@register(MedicationDetails)
class MedicationDetailsTranslation(TranslationOptions):
    fields = ('description', 'usage_instructions', 'side_effects', 'contraindications', 'storage_instructions')

@register(MedicationPrescription)
class MedicationPrescriptionTranslation(TranslationOptions):
    fields = ('institution', 'doctor', 'reason')

@register(TavsiyaEtilganDori)
class TavsiyaEtilganDoriTranslation(TranslationOptions):
    fields = ('seria_raqam',)