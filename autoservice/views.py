from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from .forms import UzsakymasReviewForm
from .models import AutomobiloModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga, Akcijos


def index(request):
    paslaugu_kiekis = Paslauga.objects.all().count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(status__exact='atlikta').count()
    automobiliu_kiekis = Automobilis.objects.all().count()
    uzregistruoti_auto = Uzsakymas.objects.filter(status__exact='uzregistruotas').count()
    tvarkomi_auto = Uzsakymas.objects.filter(status__in=['eileje', 'tvarkomas']).count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atlikti_uzsakymai': atlikti_uzsakymai,
        'automobiliu_kiekis': automobiliu_kiekis,
        'uzregistruoti_auto': uzregistruoti_auto,
        'tvarkomi_auto': tvarkomi_auto,
        'num_visits': num_visits,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all().order_by('id'), 2)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)
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
    paginate_by = 4
    template_name = 'uzsakymas_list.html'
    # queryset = Uzsakymas.objects.filter(status__in=['eileje', 'tvarkomas','uzregistruotas','galima atsiimti'])



class UzsakymasDetailView(FormMixin,generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    form_class = UzsakymasReviewForm

    def get_success_url(self):
        return reverse('uzsakymas-detail', kwargs={'pk': self.object.id})

        # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(valstybinis_nr__icontains=query)
                                                | Q(vin_kodas__icontains=query) | Q(klientas__icontains=query)
                                                | Q(automobilio_modelis_id__marke__icontains=query)
                                                | Q(automobilio_modelis_id__modelis__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})

def about(request):
    return render(request, 'about.html')


class LoanedUzsakymaiByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'user_uzsakymai.html'
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(savininkas=self.request.user).filter(status__in=['eileje', 'tvarkomas','uzregistruotas','galima atsiimti']).order_by('bus_sutvarkyta')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')



def akcijos(request):
    return render(request, 'akcijos.html')