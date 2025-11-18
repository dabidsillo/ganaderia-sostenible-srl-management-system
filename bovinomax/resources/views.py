from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Resource, ResourceLog
from django.views.generic import ListView
from .forms import ResourceLogForm

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


class ResourceLogListView(ListView):
    model = ResourceLog
    template_name = 'resources/resource_log.html'
    context_object_name = 'logs'
    ordering = ['-date']  # Orden por fecha descendente
    paginate_by = 10  # Opcional: Paginar resultados
