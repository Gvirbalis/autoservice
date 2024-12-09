from datetime import date
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class AutomobiloModelis(models.Model):
    marke = models.CharField('Markė', max_length=100, help_text='Iveskite markę (pvz. Ford )')
    modelis = models.CharField('Modelis', max_length=100, help_text='Iveskite modelį (pvz. Focus )')

    def __str__(self):
        return f'{self.marke} {self.modelis}'

    class Meta:
        verbose_name = 'Automobilio Modelis'
        verbose_name_plural = 'Automobilio modeliai'


class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis_NR', max_length=15, help_text='Iveskite Valstybini nr.(pvz AAA000)')
    automobilio_modelis_id = models.ForeignKey('AutomobiloModelis', on_delete=models.CASCADE, null=False,
                                               related_name='automobiliomodelis')
    vin_kodas = models.CharField('VIN_Kodas', max_length=17, help_text='Iveskite VIN (pvz.3C6UR5CJXEG146621)')
    klientas = models.CharField('Klientas', max_length=100, help_text='Vardas Pavarde pvz(Juozas Juozaitis)')
    aprasymas = HTMLField('Aprasymas', help_text='Aprasymas', null=True)
    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)

    def __str__(self):
        return f'Valstybinis NR: {self.valstybinis_nr}   VIN: {self.vin_kodas}   Klientas: {self.klientas}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.cover.path)
        if img.height > 225 or img.width > 400:
            output_size = (400, 225)
            img.thumbnail(output_size)
            img.save(self.cover.path)

    def display_automobilis_modelis(self):
        return f'{self.automobilio_modelis_id.marke} {self.automobilio_modelis_id.modelis}'

    display_automobilis_modelis.short_description = 'Automobilis'

    class Meta:
        verbose_name_plural = "Automobiliai"


class Uzsakymas(models.Model):
    data = models.DateField('Data', null=True, blank=True)
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.CASCADE, null=False)
    bus_sutvarkyta = models.DateField('Bus sutvarkyta', null=True, blank=True)
    savininkas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.bus_sutvarkyta and date.today() > self.bus_sutvarkyta:
            return True
        return False

    LOAN_STATUS = (
        ('uzregistruotas', 'Uzregistruota'),
        ('eileje', 'Eileje'),
        ('tvarkomas', 'Tvarkoma'),
        ('galima atsiimti', 'Galima atsiimti'),
        ('atlikta', 'Atlikta'),
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        blank=True,
        default='Uzregistruotas',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['bus_sutvarkyta']
        verbose_name_plural = "Uzsakymai"

    def __str__(self):
        return (f'Užsakymo NR.{self.id} {self.data} ,Statusas: {self.status} - '
                f'Automobilis: {self.automobilis_id.valstybinis_nr} VIN:{self.automobilis_id.vin_kodas}')

    def display_automobilis_val_nr(self):
        return self.automobilis_id.valstybinis_nr

    display_automobilis_val_nr.short_description = 'Valstybinis NR.'

    def display_automobilis_vin(self):
        return self.automobilis_id.vin_kodas

    display_automobilis_vin.short_description = 'VIN Kodas.'

    def display_automobilis_client(self):
        return self.automobilis_id.klientas

    display_automobilis_client.short_description = 'Klientas'

    def display_automobilis_marke(self):
        return self.automobilis_id.automobilio_modelis_id

    display_automobilis_marke.short_description = 'Gamintojas/Marke'


#
class UzsakymoEilute(models.Model):
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.CASCADE, null=False)
    uzsakymo_id = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, null=False)
    kiekis = models.CharField('Kiekis', max_length=250, help_text='Iveskite kieki')

    #
    def __str__(self):
        return (f'Valstybinis NR: {self.uzsakymo_id.automobilis_id.valstybinis_nr} '
                f'Paslauga: {self.paslauga_id.pavadinimas} Kiekis: {self.kiekis}')

    class Meta:
        verbose_name = 'Uzsakymo eilutes'
        verbose_name_plural = 'Uzsakymo eilute'


class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100,
                                   help_text='Iveskite paslaugos pavadinima (pvz.Tepalu keitimas)')
    kaina = models.IntegerField('Kaina', help_text='Iveskite kaina paslaugos(pvz: 199)')

    def __str__(self):
        return f'{self.pavadinimas}, Kaina: {self.kaina}'

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class UzsakymasReview(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']


class Akcijos(models.Model):
    data = models.DateField('Data', null=True, blank=True)
    aprasymas = HTMLField('Aprasymas', help_text='Aprasymas', null=True)


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/no-image.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
