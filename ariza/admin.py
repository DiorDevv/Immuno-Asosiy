from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from dori.models import MedicationType
from .models import (
    TransplantCenter,
    ToWhom,
    ApplicationStatus,
    Application,
    ApplicationMedication, MedicationTypeApp, MedicationApp
)


# class MedicationInline(admin.TabularInline):
#     model = MedicationApp
#     extra = 1
#     fields = ('name', 'medication_type')


@admin.register(MedicationTypeApp)
class MedicationTypeAppAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # inlines = [MedicationInline]


@admin.register(MedicationApp)
class MedicationAppAdmin(admin.ModelAdmin):
    list_display = ('name', 'medication_type')
    list_filter = ('medication_type',)
    search_fields = ('name',)
    extra = 1


# class ApplicationMedicationInline(admin.TabularInline):
#     model = ApplicationMedication
#     extra = 1
#     fields = ('medication', 'dosage', 'quantity', 'days_scheduled')
#     raw_id_fields = ('medication',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'director_name', 'to_center', 'date', 'status_colored', 'view_link')
    list_filter = ('status', 'to_center', 'position', 'date')
    search_fields = ('director_name', 'main_center', 'subject')
    readonly_fields = ('created_at',) if hasattr(Application, 'created_at') else ()
    date_hierarchy = 'date'
    # inlines = [ApplicationMedicationInline]
    # fieldsets = (
    #     ('Basic Information', {
    #         'fields': ('director_name', 'to_center', 'position', 'date', 'status')
    #     }),
    #     ('Center Details', {
    #         'fields': ('main_center', 'start_date', 'end_date', 'patient_count'),
    #     }),
    #     ('Additional Information', {
    #         'fields': ('subject', 'attachment', 'additional_info'),
    #         'classes': ('collapse',),
    #     }),
    # )

    def status_colored(self, obj):
        status_colors = {
            'Qabul qilindi': 'green',
            'Javob berilmadi': 'orange',
            'Rad etildi': 'red',
            # Add more status colors as needed
        }

        # Default color if status name is not in the dictionary
        color = status_colors.get(obj.status.type, 'gray')

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.status.type
        )

    status_colored.short_description = 'Status'

    def view_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}">View</a>', url)

    view_link.short_description = 'View'


@admin.register(TransplantCenter)
class TransplantCenterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ToWhom)
class ToWhomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = 'type',
    search_fields = 'type',


@admin.register(ApplicationMedication)
class ApplicationMedicationAdmin(admin.ModelAdmin):
    list_display = ('application', 'medication', 'dosage', 'quantity', 'days_scheduled')
    list_filter = ('medication', 'application__status')
    search_fields = ('application__director_name', 'medication__name')
    raw_id_fields = ('application', 'medication')
    extra = 1