from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'date_of_birth')
    search_fields = ('name', 'breed')



from .models import Vaccine, VaccineApplication

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(VaccineApplication)
class VaccineApplicationAdmin(admin.ModelAdmin):
    list_display = ('animal', 'vaccine', 'date_applied', 'notes')
    list_filter = ('date_applied', 'vaccine')
    search_fields = ('animal__name', 'vaccine__name')