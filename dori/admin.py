# from django.contrib import admin

'''
This code helpes for all models add admin row



Register your models here.
 from django.apps import apps

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
     except:
         pass

'''

from django.contrib import admin
from .models import (
    MedicationType,
    Medication,
    InventoryTransaction,
    MedicationDetails,
    MedicationPrescription,
    TavsiyaEtilganDori, Notification, Attachment
)

# Register for MedicationType
@admin.register(MedicationType)
class MedicationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Inline for MedicationDetails
class MedicationDetailsInline(admin.StackedInline):
    model = MedicationDetails
    can_delete = False
    verbose_name_plural = 'Medication Details'


# Inline for InventoryTransaction
class InventoryTransactionInline(admin.TabularInline):
    model = InventoryTransaction
    extra = 1
    fields = ('transaction_type', 'quantity', 'date', 'patient', 'notes', 'archived')
    readonly_fields = ('date',)


# Register for Medication
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'dosage', 'dosage_unit', 'warehouse_quantity')
    list_filter = ('type', 'dosage_unit')
    search_fields = ('name', 'type__name')
    readonly_fields = ('total_input', 'total_output', 'balance')
    inlines = [MedicationDetailsInline, InventoryTransactionInline]
    fieldsets = (
        (None, {
            'fields': ('type', 'name', 'dosage', 'dosage_unit')
        }),
        ('Inventory Statistics', {
            'fields': ('total_input', 'total_output', 'balance'),
            'classes': ('collapse',)
        }),
    )


# Register for InventoryTransaction
@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('medication', 'transaction_type', 'quantity', 'date', 'patient', 'archived')
    list_filter = ('transaction_type', 'date', 'archived', 'medication__type')
    search_fields = ('medication__name', 'notes', 'patient__full_name')
    date_hierarchy = 'date'
    raw_id_fields = ('patient',)
    actions = ['mark_as_archived', 'mark_as_unarchived']

    def mark_as_archived(self, request, queryset):
        queryset.update(archived=True)
    mark_as_archived.short_description = "Mark selected transactions as archived"

    def mark_as_unarchived(self, request, queryset):
        queryset.update(archived=False)
    mark_as_unarchived.short_description = "Mark selected transactions as unarchived"


# Inline for PrescribedMedication
class PrescribedMedicationInline(admin.TabularInline):
    model = TavsiyaEtilganDori
    extra = 1
    fields = ('dori_nomi', 'kunlik_dori', 'miqdori', 'qabul_qilish_muddati',
              'boshlanish', 'tugallanish', 'seria_raqam', 'yaroqlilik_muddati')
    autocomplete_fields = ('dori_nomi',)


# Register for MedicationPrescription
@admin.register(MedicationPrescription)
class MedicationPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_number', 'patient', 'prescription_date', 'institution', 'doctor', 'is_active')
    list_filter = ('prescription_date', 'is_active', 'institution')
    search_fields = ('prescription_number', 'patient__full_name', 'doctor', 'institution')
    raw_id_fields = ('patient',)
    date_hierarchy = 'prescription_date'
    inlines = [PrescribedMedicationInline]
    fieldsets = (
        (None, {
            'fields': ('patient', 'prescription_date', 'prescription_number')
        }),
        ('Details', {
            'fields': ('institution', 'doctor', 'reason', 'is_active')
        }),
    )


# Register for PrescribedMedication
@admin.register(TavsiyaEtilganDori)
class PrescribedMedicationAdmin(admin.ModelAdmin):
    list_display = ('dori_nomi', 'bemor_dori', 'kunlik_doza', 'miqdori',
                    'boshlanish', 'tugallanish', 'is_active')
    list_filter = ('boshlanish', 'tugallanish')
    search_fields = ('dori__name', 'bemor_dori__prescription_number',
                     'bemor_dori__patient__full_name')
    raw_id_fields = ('bemor_dori', 'dori_nomi')
    date_hierarchy = 'boshlanish'
    fieldsets = (
        (None, {
            'fields': ('bemor_dori', 'dori_nomi', 'kunlik_doza', 'miqdori')
        }),
        ('Administration', {
            'fields': ('qabul_qilish_muddati', 'boshlanish', 'tugallanish', 'seria_raqam', 'yaroqlilik_muddati')
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type','message', 'quantity', 'created_at', 'status')

@admin.register(Attachment)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name',)