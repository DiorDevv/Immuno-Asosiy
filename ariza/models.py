from django.db import models
from django.db.models import TextChoices
from django.utils import timezone


class TransplantCenter(models.Model): #Muassasa nomi
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Muassasa nomi'
        verbose_name_plural = 'Muassasalar nomi'

    def __str__(self):
        return self.name


class ToWhom(models.Model): #Kimga jo'natilishi
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Kimga jo'natish"
        verbose_name_plural = "Kimga jo'natish"


    def __str__(self):
        return self.name


class ApplicationStatus(models.Model): # Ariza Statusi
    class StatusType(TextChoices):
        RECEIVED = 'Received', 'received'
        CANCELED = 'Canceled', 'canceled'
        PENDING = 'Pending', 'pending'
        UNANSWERED = 'Unanswered', 'unanswered'
    type = models.CharField(max_length=255, choices=StatusType.choices)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return self.type


class MedicationTypeApp(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MedicationApp(models.Model):
    name = models.CharField(max_length=255)
    medication_type = models.ForeignKey(MedicationTypeApp, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Application(models.Model): # Ariza
    director_name = models.CharField(max_length=255)
    to_center = models.ForeignKey(TransplantCenter, on_delete=models.CASCADE, related_name='received_applications')
    position = models.ForeignKey(ToWhom, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE, related_name='aplication')
    # main_center = models.CharField(max_length=255, blank=True, null=True)
    # start_date = models.DateField(null=True, blank=True)
    # end_date = models.DateField(null=True, blank=True)
    patient_count = models.IntegerField(default=0)
    # subject = models.CharField(max_length=255, blank=True, null=True)
    # attachment = models.FileField(upload_to='applications/', null=True, blank=True,
    #                               max_length=5 * 1024 * 1024)  # 5MB limit
    # additional_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"

    def __str__(self):
        return f"Application {self.id} - {self.director_name}"


class ApplicationMedication(models.Model): # Dori uchun ariza
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='medications')
    medication = models.ForeignKey(MedicationApp, on_delete=models.CASCADE, related_name='application_medication')
    dosage = models.FloatField()  # in mg
    quantity = models.IntegerField(default=0)
    days_scheduled = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Dori uchun ariza"
        verbose_name_plural = "Dori uchun arizalar"

    def __str__(self):
        return f"{self.medication.name} - {self.dosage}mg"
