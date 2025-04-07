from django.db import models
from django.db.models import TextChoices

from users.models import Role


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


class ApplicationStatus(models.TextChoices):
    RECEIVED = 'Received', 'Qabul qilindi'
    CANCELED = 'Canceled', 'Qaytarildi'
    PENDING = 'Pending', 'Jarayonda'
    UNANSWERED = 'Unanswered', 'Javob berilmadi'






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
    director_name = models.CharField(max_length=255, null=True, blank=True)
    to_center = models.ForeignKey("TransplantCenter", on_delete=models.CASCADE, related_name='received_applications', null=True, blank=True)
    position = models.ForeignKey("ToWhom", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,  # ✅ To‘g‘ri usul
        default=ApplicationStatus.PENDING,
        null=True, blank=True
    )
    current_role = models.CharField(max_length=20, choices=Role.choices,
                                    default=Role.VRACH, null=True, blank=True)  # Default: Vrach
    # main_center = models.CharField(max_length=255, blank=True, null=True)
    # start_date = models.DateField(null=True, blank=True)
    # end_date = models.DateField(null=True, blank=True)
    patient_count = models.IntegerField(default=0, null=True, blank=True)
    # subject = models.CharField(max_length=255, blank=True, null=True)
    # attachment = models.FileField(upload_to='applications/', null=True, blank=True,
    #                               max_length=5 * 1024 * 1024)  # 5MB limit
    # additional_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"

    def __str__(self):
        return f"Application {self.id} - {self.director_name}"

    def approve(self):
        """Arizani keyingi bosqichga o'tkazish"""
        role_sequence = [Role.VRACH, Role.TTB, Role.VSSB, Role.UZMED, Role.VAZIR]

        if self.status == ApplicationStatus.CANCELED:
            return "Bu ariza rad etilgan."

        if self.current_role == Role.VAZIR:
            return "Ariza allaqachon yakunlangan."

        next_role_index = role_sequence.index(self.current_role) + 1
        if next_role_index < len(role_sequence):
            self.current_role = role_sequence[next_role_index]
            self.status = ApplicationStatus.UNANSWERED  # Har safar yangi rolga o'tganda, status yana "Javob berilmadi" bo'ladi.
            self.save()
            return f"Ariza {self.current_role} ga yuborildi."

        return "Ariza jarayoni yakunlandi."

    def reject(self):
        """Arizani rad qilish"""
        self.status = ApplicationStatus.CANCELED
        self.save()
        return "Ariza rad qilindi."


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
