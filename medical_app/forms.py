from django import forms
from .models import PatientData

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = '__all__'
        exclude = ['diagnosis', 'prediction_made', 'created_at']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 120}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_pressure': forms.NumberInput(attrs={'class': 'form-control', 'min': 50, 'max': 250}),
            'cholesterol': forms.NumberInput(attrs={'class': 'form-control', 'min': 100, 'max': 400}),
            'blood_sugar': forms.NumberInput(attrs={'class': 'form-control', 'min': 50, 'max': 300}),
        }