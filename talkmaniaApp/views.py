from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import HabitacionForm, ReservaForm, HotelForm

# Create your views here.
def vista_hotel(request):
    hoteles = Hotel.objects.filter(estado=True)
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
            messages.success(request, f'Habitación {habitacion.numero} agregada exitosamente.')
            return redirect('detalle_hotel', hotel_id=habitacion.hotel.id)
    else:
        form = HabitacionForm()
    
    return render(request, 'hotel/agregar_habitacion.html', {'form': form})

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
                messages.error(request, 'Debes tener un perfil de cliente para hacer reservas.')
                return redirect('home')
            
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
            
            # Enviar correo de confirmación
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                # Obtener la hora actual
                hora_reserva = timezone.now().strftime('%H:%M')
                
                # Construir el mensaje del correo
                asunto = f'Confirmación de Reserva - {habitacion.hotel.nombre}'
                mensaje = f"""
Hola {request.user.username},

¡Tu reserva ha sido confirmada exitosamente!

DETALLES DE LA RESERVA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Fecha de reserva: {reserva.fecha_reserva.strftime('%d/%m/%Y')}
🕐 Hora de reserva: {hora_reserva}

🏨 Hotel: {habitacion.hotel.nombre}
📍 Dirección: {habitacion.hotel.direccion}
⭐ Estrellas: {habitacion.hotel.estrellas}

🛏️ Habitación: #{habitacion.numero} - {habitacion.get_tipo_display()}
💰 Precio por noche: ${habitacion.precio}

CHECK-IN: {reserva.fecha_entrada.strftime('%d/%m/%Y')}
CHECK-OUT: {reserva.fecha_salida.strftime('%d/%m/%Y')}
📊 Total de noches: {dias}
💵 Monto total: ${reserva.monto}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Contacto del hotel: {habitacion.hotel.telefono}
📧 Email del hotel: {habitacion.hotel.email}

¡Gracias por elegir Talkmania!
Esperamos que disfrutes tu estadía.

---
Este es un correo automático, por favor no responder.
                """
                
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@talkmania.com',
                    [request.user.email],
                    fail_silently=True,  # No fallar si el email no se puede enviar
                )
                messages.success(request, f'¡Reserva confirmada exitosamente! Se ha enviado un correo de confirmación a {request.user.email}')
            except Exception as e:
                # Si falla el envío del correo, aún así mostrar mensaje de éxito de la reserva
                messages.success(request, '¡Reserva confirmada exitosamente!')
                messages.warning(request, f'No se pudo enviar el correo de confirmación: {str(e)}')
            
            return redirect('historial_reservas')
    else:
        form = ReservaForm()
    
    return render(request, 'hotel/confirmar_reserva.html', {'form': form, 'habitacion': habitacion})

# Gestión de Hoteles (solo administradores)
@login_required
def crear_hotel(request):
    if request.user.rol != 'administrador':
        messages.error(request, 'No tienes permisos para crear hoteles.')
        return redirect('vista_hotel')
    
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.admin = request.user  # Asignar el usuario actual como admin del hotel
            hotel.save()
            messages.success(request, f'Hotel "{hotel.nombre}" creado exitosamente.')
            return redirect('vista_hotel')
    else:
        form = HotelForm()
    
    return render(request, 'hotel/crear_hotel.html', {'form': form})

@login_required
def editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Verificar que el usuario sea admin y sea el dueño del hotel o superadmin
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para editar este hotel.')
        return redirect('vista_hotel')
    
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hotel "{hotel.nombre}" actualizado exitosamente.')
            return redirect('detalle_hotel', hotel_id=hotel.id)
    else:
        form = HotelForm(instance=hotel)
    
    return render(request, 'hotel/editar_hotel.html', {'form': form, 'hotel': hotel})

@login_required
def eliminar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Verificar que el usuario sea admin y sea el dueño del hotel o superadmin
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para eliminar este hotel.')
        return redirect('vista_hotel')
    
    if request.method == 'POST':
        nombre = hotel.nombre
        hotel.delete()
        messages.success(request, f'Hotel "{nombre}" eliminado exitosamente.')
        return redirect('vista_hotel')
    
    return render(request, 'hotel/eliminar_hotel.html', {'hotel': hotel})