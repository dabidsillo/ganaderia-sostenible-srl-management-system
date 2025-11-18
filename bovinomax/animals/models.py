from django.db import models
from django.urls import reverse



class Animal(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='animals/photos/', blank=True, null=True)


    def get_absolute_url(self):
        return reverse('animals:animal_detail', args=[self.id])
    
    def __str__(self):
        return self.name


class Vaccine(models.Model):
    name = models.CharField(max_length=100, default='Vacuna desconocida')  # Valor predeterminado
    description = models.TextField()

    def __str__(self):
        return self.name

class VaccineApplication(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='vaccine_applications')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date_applied = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vaccine.name} - {self.animal.name} ({self.date_applied})"