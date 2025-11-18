# bovinomax/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Vista para la página principal
def home(request):
    return render(request, 'home.html')
