from django import forms
from .models import VaccineApplication

class VaccineApplicationForm(forms.ModelForm):
    class Meta:
        model = VaccineApplication
        fields = ['vaccine', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
