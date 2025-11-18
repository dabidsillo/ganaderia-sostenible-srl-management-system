from django.contrib import admin
from .models import Animal, Vaccine

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'date_of_birth')
    search_fields = ('name', 'breed')

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')