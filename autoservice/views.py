from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic

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


def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    # print(automobiliai)
    return render(request, 'automobiliai.html', context=context)


def automobilis(request, automobilis_id):
    single_automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    # print(single_automobilis)
    return render(request, 'automobilis.html', {'automobilis': single_automobilis})


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    template_name = 'uzsakymas_list.html'
    # queryset = Uzsakymas.objects.filter(status__in=['eileje', 'tvarkomas','uzregistruotas','galima atsiimti'])


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
