from django.contrib import admin
from .models import Resource, ResourceLog

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_quantity')

@admin.register(ResourceLog)
class ResourceLogAdmin(admin.ModelAdmin):
    list_display = ('resource', 'quantity', 'date', 'description')
    list_filter = ('resource', 'date')
