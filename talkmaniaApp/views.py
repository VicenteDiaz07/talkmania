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