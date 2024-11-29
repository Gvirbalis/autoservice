from django.shortcuts import render
from django.http import HttpResponse
from .models import AutomobiloModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga


def index(request):
    paslaugu_kiekis = Paslauga.objects.all().count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(status__exact='atlikta').count()
    automobiliu_kiekis = Automobilis.objects.all().count()
    uzregistruoti_auto = Uzsakymas.objects.filter(status__exact='uzregistruotas').count()
    tvarkomi_auto = Uzsakymas.objects.filter(status__in=['eileje', 'tvarkomas']).count()

    # # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atlikti_uzsakymai': atlikti_uzsakymai,
        'automobiliu_kiekis': automobiliu_kiekis,
        'uzregistruoti_auto': uzregistruoti_auto,
        'tvarkomi_auto': tvarkomi_auto,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

# Create your views here.
