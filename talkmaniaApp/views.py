from django.shortcuts import render, redirect
from .models import *
from .forms import HabitacionForm

# Create your views here.
def vista_hotel(request):
    hoteles = Hotel.objects.all()
    return render(request, 'hotel/hoteles.html', {'hoteles': hoteles})

def vista_detalle_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    # Logic to get 6 available rooms. 
    # For now, we can filter by the hotel and limit to 6, or create mock data if not enough rooms exist.
    # Assuming we want to show actual rooms from DB if possible, but ensuring 6 are shown as requested.
    habitaciones = Habitacion.objects.filter(hotel=hotel, estado='D')[:6]
    
    return render(request, 'hotel/detalle_hotel.html', {'hotel': hotel, 'habitaciones': habitaciones})

def agregar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
from django.shortcuts import render, redirect
from .models import *
from .forms import HabitacionForm

# Create your views here.
def vista_hotel(request):
    hoteles = Hotel.objects.all()
    return render(request, 'hotel/hoteles.html', {'hoteles': hoteles})

def vista_detalle_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    # Logic to get 6 available rooms. 
    # For now, we can filter by the hotel and limit to 6, or create mock data if not enough rooms exist.
    # Assuming we want to show actual rooms from DB if possible, but ensuring 6 are shown as requested.
    habitaciones = Habitacion.objects.filter(hotel=hotel, estado='D')[:6]
    
    return render(request, 'hotel/detalle_hotel.html', {'hotel': hotel, 'habitaciones': habitaciones})

def agregar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            habitacion = form.save()
            return redirect('detalle_hotel', hotel_id=habitacion.hotel.id)
    else:
        form = HabitacionForm()
    
    return render(request, 'hotel/agregar_habitacion.html', {'form': form})

from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def confirmar_reserva(request, habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            
            # Asignar cliente (usuario actual)
            try:
                reserva.Cliente = request.user.cliente
            except:
                # Si no tiene cliente, redirigir o manejar error (aquí asumimos que tiene)
                return redirect('home') # O mostrar error
            
            reserva.Hotel = habitacion.hotel
            reserva.fecha_reserva = timezone.now().date()
            
            # Calcular monto (días * precio)
            dias = (reserva.fecha_salida - reserva.fecha_entrada).days
            if dias < 1: dias = 1
            reserva.monto = dias * habitacion.precio
            
            reserva.save()
            
            # Crear relación Reserva_Habitacion
            Reserva_Habitacion.objects.create(reserva=reserva, habitacion=habitacion)
            
            # Marcar habitación como reservada (opcional, depende de la lógica de negocio)
            # habitacion.estado = 'R'
            # habitacion.save()
            
            return redirect('historial_reservas')
    else:
        form = ReservaForm()
    
    return render(request, 'hotel/confirmar_reserva.html', {'form': form, 'habitacion': habitacion})