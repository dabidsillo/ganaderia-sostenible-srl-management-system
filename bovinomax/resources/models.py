from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre del recurso (agua, comida, etc.)
    current_quantity = models.FloatField(default=0)  # Cantidad actual del recurso

    def __str__(self):
        return f"{self.name} - {self.current_quantity}"

class ResourceLog(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='logs')
    quantity = models.FloatField()  # Positivo para ingresos, negativo para egresos
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        action = "Ingreso" if self.quantity > 0 else "Egreso"
        return f"{action} de {abs(self.quantity)} ({self.resource.get_name_display()})"
