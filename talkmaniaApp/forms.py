from django import forms
from talkmaniaApp.models import *

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['hotel', 'numero', 'tipo', 'precio', 'estado']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de habitación'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio por noche'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_entrada', 'fecha_salida', 'tipo_pago']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
        }


