from django.db.models import Model, CharField, IntegerField, DateField, OneToOneField, CASCADE



class Shifokor_qoshish(Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    jshshir = CharField(max_length=14)
    familya = CharField(max_length=50)
    ismi = CharField(max_length=50)
    otasining_ismi = CharField(max_length=50)
    jinsi = CharField(max_length=1, choices=GENDER_CHOICES)
    tugilgan_sana = DateField()

    def __str__(self):
        return f"{self.ismi} {self.familya} - {self.jshshir}"


class Shifokorlar(Model):
    shifokor = OneToOneField('Shifokor_qoshish', CASCADE, related_name='shifokor')
    lavozimi = CharField(max_length=100)
    mutaxasislik_toifasi = CharField(max_length=100)
    telefon_raqami = CharField(max_length=13)
    biriktirilgan_muassasa = CharField(null=True)
    ish_staji = IntegerField()
    oxirgi_malaka_oshirgan_joyi = CharField(max_length=150)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        a = self.user.name
        obj = self.object
        obj.mutaxasislik_toifasi = a
        obj.save(self, *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,)

