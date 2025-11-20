from django.db import models
from datetime import date

class Animal(models.Model):
    """Modelo que representa un animal en la granja."""
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='animals/photos/', blank=True, null=True)
    is_pregnant = models.BooleanField(default=False)

    def calculate_age(self):
        """Calcula la edad del animal en años."""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.name


class DailyFeed(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    STATUS_CHOICES = [
        (PENDING, "Pendiente"),
        (COMPLETED, "Completado"),
    ]

    animal = models.OneToOneField(Animal, on_delete=models.CASCADE)
    food_amount = models.FloatField(default=0)  # Comida en kg
    water_amount = models.FloatField(default=0)  # Agua en litros
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    date = models.DateField(auto_now_add=True)  # Fecha de la alimentación

    def __str__(self):
        return f"Alimentación de {self.animal.name} - {self.date} ({self.get_status_display()})"



from django.db import models
from django.urls import reverse

class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('animals:vaccine_list')

class VaccineApplication(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='vaccine_applications')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='applications')
    date_applied = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vaccine.name} aplicado a {self.animal.name} el {self.date_applied}"



