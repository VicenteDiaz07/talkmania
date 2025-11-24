from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Review

class RegistroForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre completo (ej: Juan Pérez)'}),
        label='Nombre completo'
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Teléfono (opcional)'}))
    
    class Meta:
        model = User
        fields = ['username', 'nombre_completo', 'email', 'telefono', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario (sin espacios)'}),
        }
        help_texts = {
            'username': 'Nombre de usuario para iniciar sesión (sin espacios, ej: juan_perez)',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Dividir el nombre completo en first_name y last_name
        nombre_completo = self.cleaned_data.get('nombre_completo', '')
        partes = nombre_completo.strip().split(' ', 1)  # Dividir en máximo 2 partes
        
        user.first_name = partes[0] if len(partes) > 0 else ''
        user.last_name = partes[1] if len(partes) > 1 else ''
        
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Usuario o contraseña incorrectos')
            if self.user.bloqueado:
                raise forms.ValidationError('Tu cuenta está bloqueada. Contacta al administrador.')
        return self.cleaned_data
    
    def get_user(self):
        return self.user


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comparte tu experiencia...'}),
        }
        labels = {
            'calificacion': 'Calificación (1-5 estrellas)',
            'comentario': 'Comentario',
        }