from django.db import models


class Automobilo_modelis(models.Model):
    marke = models.CharField('Markė', max_length=100,help_text='Iveskite markę (pvz. Ford )')
    modelis = models.CharField('Modelis', max_length=100,help_text='Iveskite modelį (pvz. Focus )')


    def __str__(self):
        return f'{self.marke} {self.modelis}'

class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis_NR', max_length=15,help_text='Iveskite Valstybini nr.(pvz AAA000)')
    automobilio_modelis_id = models.ForeignKey('Automobilo_modelis', on_delete=models.CASCADE, null=False)
    vin_kodas = models.CharField('VIN_Kodas', max_length=17,help_text='Iveskite VIN (pvz.3C6UR5CJXEG146621)')
    klientas = models.CharField('Klientas', max_length=100,help_text='Vardas Pavarde pvz(Juozas Juozaitis)')

    def __str__(self):
        return f'Valstybinis NR: {self.valstybinis_nr}   VIN: {self.vin_kodas}   Klientas: {self.klientas}'

class Uzsakymas(models.Model):
    data = models.DateField('Bus sutvarkyta',null=True, blank=True)
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.CASCADE, null=False)

    LOAN_STATUS = (
        ('uzregistruotas', 'Uzregistruota'),
        ('eileje', 'Eileje'),
        ('tvarkomas', 'Tvarkoma'),
        ('Galima atsiimti', 'Galima atsiimti'),
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        blank=True,
        default='uzregistruotas',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['data']
    def __str__(self):
        return f'Užsakymas {self.id} ({self.status}) - Automobilis: {self.automobilis_id.valstybinis_nr} VIN:{self.automobilis_id.vin_kodas}'

#
class Uzsakymo_eilute(models.Model):
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.CASCADE, null=False)
    uzsakymo_id = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, null=False)
    kiekis = models.CharField('Kiekis',max_length=250,help_text='Iveskite kieki')
#
    def __str__(self):
        return (f'Valstybinis NR: {self.uzsakymo_id.automobilis_id.valstybinis_nr} '
                f'Paslauga: {self.paslauga_id.pavadinimas} Kiekis: {self.kiekis}')

class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100,help_text='Iveskite paslaugos pavadinima (pvz.Tepalu keitimas)')
    kaina = models.IntegerField('Kaina',help_text='Iveskite kaina paslaugos(pvz: 199)')

    def __str__(self):
        return f'{self.pavadinimas}, Kaina: {self.kaina}'