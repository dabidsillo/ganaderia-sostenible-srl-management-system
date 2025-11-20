from django import forms
from .models import VaccineApplication

from .models import VaccineApplication

class VaccineApplicationForm(forms.ModelForm):
    class Meta:
        model = VaccineApplication
        fields = ['vaccine', 'notes']
