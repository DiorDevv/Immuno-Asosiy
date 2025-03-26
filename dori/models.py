from django.db import models
from django.db.models import Sum
from django.utils import timezone

from bemor.models import Bemor


class MedicationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Medication(models.Model):
    type = models.ForeignKey(MedicationType, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    dosage_unit = models.CharField(max_length=10, default='mg')

    def __str__(self):
        return f"{self.name} {self.dosage}{self.dosage_unit}"


    def total_input(self):
        return self.inventory_transactions.filter(transaction_type='INPUT').aggregate(
            total=Sum('quantity'))['total'] or 0

    def total_output(self):
        return self.inventory_transactions.filter(transaction_type='OUTPUT').aggregate(
            total=Sum('quantity'))['total'] or 0

    def balance(self):
        return self.total_input() - self.total_output()

    def warehouse_quantity(self):
        return self.balance()




class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('INPUT', 'Kirim'),
        ('OUTPUT', 'Chiqim'),
    ]

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='inventory_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    patient = models.ForeignKey(Bemor, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='medication_transactions')

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.medication.name} - {self.quantity}"

    class Meta:
        ordering = ['-date']


class MedicationDetails(models.Model):
    """Additional details about medications that can be displayed in the info panel"""
    medication = models.OneToOneField(Medication, on_delete=models.CASCADE, related_name='details')
    description = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"Details for {self.medication}"


class MedicationPrescription(models.Model):
    patient = models.ForeignKey(Bemor, on_delete=models.CASCADE, related_name='prescriptions')
    prescription_date = models.DateField(default=timezone.now)
    prescription_number = models.CharField(max_length=20)
    institution = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    reason = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"#{self.prescription_number}"

    class Meta:
        ordering = ['-prescription_date']


class TavsiyaEtilganDori(models.Model):
    bemor_dori = models.ForeignKey(MedicationPrescription, on_delete=models.CASCADE, related_name='medications')
    dori_nomi = models.ForeignKey(Medication, on_delete=models.CASCADE)
    kunlik_doza = models.DecimalField(max_digits=10, decimal_places=2)
    miqdori = models.PositiveIntegerField()
    seria_raqam = models.CharField(max_length=20, blank=True)
    qabul_qilish_muddati = models.PositiveIntegerField(help_text="Duration in days")
    boshlanish = models.DateField()
    tugallanish = models.DateField()
    yaroqlilik_muddati = models.TextField(blank=True)

    def __str__(self):
        return f"{self.dori_nomi.name} - {self.kunlik_doza}{self.dori_nomi.dosage_unit}"

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.boshlanish <= today <= self.tugallanish


#  Notifications
class Notification(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rejected'),
    )

    TYPE_CHOICES = (
        ('entry', 'Entry'),
        ('exit', 'Exit'),
    )

    id = models.AutoField(primary_key=True)
    notification_type = models.CharField("Notification Type", max_length=10, choices=TYPE_CHOICES, default='entry')
    message = models.CharField("Ma'lumot", max_length=255)
    quantity = models.IntegerField("Miqdori", default=10)
    created_at = models.DateTimeField("Sana", auto_now_add=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Fields for detailed view
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Medication"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.id} - {self.message}"


class Attachment(models.Model):

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="Notification"
    )
    file = models.FileField("File", upload_to='notifications/')
    name = models.CharField("Name", max_length=255)
    uploaded_at = models.DateTimeField("Uploaded At", auto_now_add=True)

    def __str__(self):
        return self.name