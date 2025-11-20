from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Resource, ResourceLog
from django.views.generic import ListView
from .forms import ResourceLogForm
from animals.models import Animal
import json
from animals.utils import prepare_animal_data, get_consumption_from_ai
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_date


def manage_resources(request):
    if request.method == 'POST':
        form = ResourceLogForm(request.POST)
        if form.is_valid():
            resource_log = form.save()

            # Actualizar la cantidad actual del recurso
            resource = resource_log.resource
            resource.current_quantity += resource_log.quantity
            resource.save()

            return redirect(reverse('resources:manage_resources'))
    else:
        form = ResourceLogForm()

    # Obtener todos los recursos con sus cantidades actuales
    resources = Resource.objects.all()
    return render(request, 'resources/manage_resources.html', {
        'form': form,
        'resources': resources,
    })




from django.db.models import Q
from django.shortcuts import render
from django.utils.dateparse import parse_date

class ResourceLogListView(ListView):
    model = ResourceLog
    template_name = 'resources/resource_log.html'
    context_object_name = 'logs'
    ordering = ['-date']  # Orden por fecha descendente

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Filtrar por rango de fechas si se proporcionan
        if start_date or end_date:
            if start_date:
                start_date = parse_date(start_date)
            if end_date:
                end_date = parse_date(end_date)
            
            queryset = queryset.filter(date__range=(start_date, end_date))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context

from django.shortcuts import render
from resources.models import Resource
from animals.utils import predict_weekly_feed

def dashboard(request):
    """
    Vista del dashboard con recursos actuales y predicciones semanales.
    """
    # Coordenadas de la granja
    latitude = 40.7128
    longitude = -74.0060

    # Obtener recursos actuales
    food_resource = Resource.objects.get(name="Comida Balanceada")
    water_resource = Resource.objects.get(name="Agua")

    # Predicciones para los próximos 7 días
    weekly_predictions = predict_weekly_feed(latitude, longitude)

    # Preparar listas para los gráficos
    prediction_dates = [pred["date"] for pred in weekly_predictions]
    food_predictions = [pred["food"] for pred in weekly_predictions]
    water_predictions = [pred["water"] for pred in weekly_predictions]

    # Días restantes basados en el primer día de consumo estimado
    days_of_food = 0
    days_of_water = 0

    if weekly_predictions:
        first_day_food = weekly_predictions[0]['food'] if weekly_predictions[0]['food'] > 0 else 1
        first_day_water = weekly_predictions[0]['water'] if weekly_predictions[0]['water'] > 0 else 1
        days_of_food = int(food_resource.current_quantity / first_day_food)
        days_of_water = int(water_resource.current_quantity / first_day_water)

    return render(request, 'resources/dashboard.html', {
        'food_resource': food_resource,
        'water_resource': water_resource,
        'weekly_predictions': weekly_predictions,
        'prediction_dates': prediction_dates,
        'food_predictions': food_predictions,
        'water_predictions': water_predictions,
        'days_of_food': days_of_food,
        'days_of_water': days_of_water,
    })
