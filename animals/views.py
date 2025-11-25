from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal, DailyFeed, VaccineApplication
from resources.models import Resource
from .utils import get_weather_data, prepare_animal_data, get_consumption_from_ai
from datetime import date, datetime
from resources.models import Resource, ResourceLog
from django.views.generic import ListView
from django.db import IntegrityError

def generate_daily_feed(request):
    """Genera la alimentación diaria consultando a la IA."""
    CHATGPT_API_KEY = ""
    city = "Santa Cruz, Bolivia"

    # Obtener datos del clima
    weather_data = get_weather_data(city)
    if not weather_data:
        return render(request, 'animals/generate_feed.html', {
            'error': "No se pudieron obtener los datos del clima.",
        })

    # Obtener todos los animales
    animals = Animal.objects.all()
    
    # Generar alimentación para cada animal
    for animal in animals:
        # Verificar si ya existe un registro para el animal en la fecha actual
        daily_feed_exists = DailyFeed.objects.filter(animal=animal, date=date.today()).exists()
        
        if not daily_feed_exists:
            animal_data = prepare_animal_data(animal, weather_data)
            food_amount, water_amount = get_consumption_from_ai(CHATGPT_API_KEY, animal_data)
            
            try:
                DailyFeed.objects.create(
                    animal=animal,
                    food_amount=food_amount,
                    water_amount=water_amount,
                    date=date.today(),  # Agregar la fecha explícitamente
                    status=DailyFeed.PENDING
                )
            except IntegrityError:
                print(f"Registro duplicado detectado para el animal: {animal.id}")

    return redirect('animals:daily_feed')


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from animals.models import DailyFeed
from resources.models import Resource, ResourceLog

def complete_feed(request, feed_id):
    feed = get_object_or_404(DailyFeed, id=feed_id)

    # Verifica que la alimentación no haya sido completada previamente
    if feed.status == DailyFeed.COMPLETED:
        return JsonResponse({"error": "Este animal ya ha sido alimentado."}, status=400)

    # Obtiene los recursos necesarios (comida y agua)
    try:
        food_resource = Resource.objects.get(name="Comida Balanceada")
        water_resource = Resource.objects.get(name="Agua")
    except Resource.DoesNotExist:
        return redirect('animals:daily_feed')

    # Verifica si hay suficientes recursos
    if food_resource.current_quantity < feed.food_amount or water_resource.current_quantity < feed.water_amount:
        return redirect('animals:daily_feed')

    # Resta los recursos necesarios
    food_resource.current_quantity -= feed.food_amount
    water_resource.current_quantity -= feed.water_amount
    food_resource.save()
    water_resource.save()

    # Registra los egresos en el historial de recursos
    ResourceLog.objects.create(
        resource=food_resource,
        quantity=-feed.food_amount,
        description=f"Alimentación de {feed.animal.name}"
    )
    ResourceLog.objects.create(
        resource=water_resource,
        quantity=-feed.water_amount,
        description=f"Alimentación de {feed.animal.name}"
    )

    # Marca la alimentación como completada
    feed.status = DailyFeed.COMPLETED
    feed.save()

    return redirect('animals:daily_feed')




def daily_feed(request):
    """Muestra la alimentación generada para una fecha específica (predeterminada: hoy)."""
    # Obtener la fecha del filtro de los parámetros GET, por defecto la fecha actual
    date_filter = request.GET.get("date", date.today().strftime('%Y-%m-%d'))

    # Convertir la fecha a un objeto `date`
    try:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
    except ValueError:
        date_filter = date.today()

    # Filtrar alimentaciones por la fecha seleccionada
    feeds = DailyFeed.objects.filter(date=date_filter)

    return render(request, 'animals/daily_feed.html', {
        'feeds': feeds,
        'date_filter': date_filter,
    })


class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'




from .forms import VaccineApplicationForm

def manage_vaccines(request, animal_id):
    """
    Vista para listar las aplicaciones de vacunas de un animal
    y registrar una nueva aplicación.
    """
    animal = get_object_or_404(Animal, id=animal_id)
    applications = VaccineApplication.objects.filter(animal=animal)

    if request.method == 'POST':
        form = VaccineApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.animal = animal
            application.save()
            return redirect('animals:manage_vaccines', animal_id=animal.id)
    else:
        form = VaccineApplicationForm()

    return render(request, 'animals/manage_vaccines.html', {
        'animal': animal,
        'applications': applications,
        'form': form,
    })