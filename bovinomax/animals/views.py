from django.views.generic import ListView, DetailView, CreateView, FormView
from .models import Animal,  VaccineApplication
from django.urls import reverse_lazy
from .forms import VaccineApplicationForm
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'

class AnimalDetailView(DetailView, FormView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    form_class = VaccineApplicationForm

    def get(self, request, *args, **kwargs):
        # Configura explícitamente el objeto del detalle
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Configura explícitamente el objeto del detalle para manejar POST
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Incluye el objeto y las aplicaciones de vacunas en el contexto
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context['vaccine_applications'] = VaccineApplication.objects.filter(animal=self.object)
        return context

    def form_valid(self, form):
        # Asocia el formulario con el animal actual y guárdalo
        form.instance.animal = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige de vuelta a la misma página
        return reverse('animals:animal_detail', args=[self.object.id])
    


def apply_vaccine(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == 'POST':
        form = VaccineApplicationForm(request.POST)
        if form.is_valid():
            # Asocia el formulario con el animal actual y guarda
            application = form.save(commit=False)
            application.animal = animal
            application.save()
            # Redirige a la página de detalle del animal
            return redirect(reverse('animals:animal_detail', args=[pk]))
    else:
        form = VaccineApplicationForm()

    return render(request, 'animals/apply_vaccine.html', {'form': form, 'animal': animal})



class AnimalCreateView(CreateView):
    model = Animal
    fields = ['name', 'breed', 'date_of_birth', 'description', 'photo']
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animals:animal_list')
