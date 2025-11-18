from django import forms
from .models import ResourceLog

class ResourceLogForm(forms.ModelForm):
    class Meta:
        model = ResourceLog
        fields = ['resource', 'quantity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
