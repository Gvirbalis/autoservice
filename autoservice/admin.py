from django.contrib import admin

# Register your models here.
from .models import AutomobiloModelis, Automobilis, Uzsakymas, Paslauga, UzsakymoEilute


class UzsakymasInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0
    can_delete = False


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data', 'status', 'display_automobilis_val_nr','display_automobilis_marke' ,
        'display_automobilis_vin', 'display_automobilis_client')
    inlines = [UzsakymasInline]
    list_filter = ('data', 'status')
    list_editable = ('status',)


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('valstybinis_nr', 'display_automobilis_modelis', 'vin_kodas', 'klientas')
    list_filter = ('klientas', 'automobilio_modelis_id')
    search_fields = ('valstybinis_nr', 'vin_kodas', 'klientas')

    fieldsets = (
        ('Automobilio Info', {'fields': ('valstybinis_nr', 'automobilio_modelis_id', 'vin_kodas','cover')}),
        ('Klientas', {'fields': ('klientas',)}),
    )


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(AutomobiloModelis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga, PaslaugaAdmin)
