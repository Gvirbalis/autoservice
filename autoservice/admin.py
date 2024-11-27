from django.contrib import admin

# Register your models here.
from .models import Automobilo_modelis, Automobilis, Uzsakymas,Paslauga,Uzsakymo_eilute

admin.site.register(Automobilis)
admin.site.register(Automobilo_modelis)
admin.site.register(Uzsakymas)
admin.site.register(Uzsakymo_eilute)
admin.site.register(Paslauga)