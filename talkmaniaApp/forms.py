from django import forms
from talkmaniaApp.models import Habitacion, Reserva, Hotel

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

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nombre', 'direccion', 'telefono', 'email', 'estrellas', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del hotel'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '912345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hotel@ejemplo.com'}),
            'estrellas': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del hotel...'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del Hotel',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Email',
            'estrellas': 'Estrellas',
            'descripcion': 'Descripción',
            'estado': 'Hotel Activo',
        }
