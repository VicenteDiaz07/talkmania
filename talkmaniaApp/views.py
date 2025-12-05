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
    
    # Obtener fechas del formulario de búsqueda
    fecha_entrada_str = request.GET.get('fecha_entrada')
    fecha_salida_str = request.GET.get('fecha_salida')
    
    # Inicializar variables
    fecha_entrada = None
    fecha_salida = None
    habitaciones_filtradas = False
    
    # Si se proporcionaron fechas, filtrar habitaciones disponibles
    if fecha_entrada_str and fecha_salida_str:
        try:
            from datetime import datetime
            fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
            
            # Validar que las fechas sean lógicas
            if fecha_salida <= fecha_entrada:
                messages.warning(request, 'La fecha de salida debe ser posterior a la fecha de entrada.')
                habitaciones = Habitacion.objects.filter(hotel=hotel, estado='D')[:6]
            else:
                # Obtener IDs de habitaciones ocupadas en el rango de fechas
                habitaciones_ocupadas_ids = Reserva.objects.filter(
                    Hotel=hotel,
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                ).values_list('reserva_habitacion__habitacion__id', flat=True)
                
                # Filtrar habitaciones disponibles (excluir las ocupadas)
                habitaciones = Habitacion.objects.filter(
                    hotel=hotel, 
                    estado='D'
                ).exclude(id__in=habitaciones_ocupadas_ids)[:6]
                
                habitaciones_filtradas = True
                
                if not habitaciones.exists():
                    messages.info(request, f'No hay habitaciones disponibles del {fecha_entrada.strftime("%d/%m/%Y")} al {fecha_salida.strftime("%d/%m/%Y")}. Intenta con otras fechas.')
                else:
                    messages.success(request, f'Mostrando {habitaciones.count()} habitación(es) disponible(s) para tus fechas.')
                    
        except ValueError:
            messages.error(request, 'Formato de fecha inválido. Por favor, selecciona las fechas correctamente.')
            habitaciones = Habitacion.objects.filter(hotel=hotel, estado='D')[:6]
    else:
        # Si no hay fechas, mostrar todas las habitaciones disponibles
        habitaciones = Habitacion.objects.filter(hotel=hotel, estado='D')[:6]
    
    # Verificar si el usuario es admin del hotel
    is_hotel_admin = False
    if request.user.is_authenticated and request.user.rol == 'administrador':
        if hotel.admin == request.user or request.user.is_superuser:
            is_hotel_admin = True
    
    return render(request, 'hotel/detalle_hotel.html', {
        'hotel': hotel,
        'habitaciones': habitaciones,
        'is_hotel_admin': is_hotel_admin,
        'fecha_entrada': fecha_entrada,
        'fecha_salida': fecha_salida,
        'habitaciones_filtradas': habitaciones_filtradas,
    })

# CRUD de Habitaciones
@login_required
def agregar_habitacion(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Verificar que el usuario sea admin y sea el dueño del hotel o superadmin
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para agregar habitaciones a este hotel.')
        return redirect('detalle_hotel', hotel_id=hotel.id)
    
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            habitacion = form.save(commit=False)
            habitacion.hotel = hotel  # Asignar el hotel automáticamente
            habitacion.save()
            messages.success(request, f'Habitación #{habitacion.numero} agregada exitosamente.')
            return redirect('detalle_hotel', hotel_id=hotel.id)
    else:
        # Pre-seleccionar el hotel en el formulario
        form = HabitacionForm(initial={'hotel': hotel})
    
    return render(request, 'hotel/agregar_habitacion.html', {'form': form, 'hotel': hotel})

@login_required
def editar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    hotel = habitacion.hotel
    
    # Verificar que el usuario sea admin y sea el dueño del hotel o superadmin
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para editar esta habitación.')
        return redirect('detalle_hotel', hotel_id=hotel.id)
    
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Habitación #{habitacion.numero} actualizada exitosamente.')
            return redirect('detalle_hotel', hotel_id=hotel.id)
    else:
        form = HabitacionForm(instance=habitacion)
    
    return render(request, 'hotel/editar_habitacion.html', {'form': form, 'habitacion': habitacion, 'hotel': hotel})

@login_required
def eliminar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    hotel = habitacion.hotel
    
    # Verificar que el usuario sea admin y sea el dueño del hotel o superadmin
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para eliminar esta habitación.')
        return redirect('detalle_hotel', hotel_id=hotel.id)
    
    if request.method == 'POST':
        numero = habitacion.numero
        habitacion.delete()
        messages.success(request, f'Habitación #{numero} eliminada exitosamente.')
        return redirect('detalle_hotel', hotel_id=hotel.id)
    
    return render(request, 'hotel/eliminar_habitacion.html', {'habitacion': habitacion, 'hotel': hotel})

# Función auxiliar para verificar disponibilidad
def verificar_disponibilidad(habitacion, fecha_entrada, fecha_salida, reserva_id=None):
    """
    Verifica si una habitación está disponible en el rango de fechas especificado.
    
    Args:
        habitacion: Objeto Habitacion a verificar
        fecha_entrada: Fecha de check-in
        fecha_salida: Fecha de check-out
        reserva_id: ID de reserva a excluir (para ediciones)
    
    Returns:
        tuple: (disponible: bool, reservas_conflictivas: QuerySet)
    """
    # Buscar reservas que se solapen con las fechas solicitadas
    reservas_conflictivas = Reserva.objects.filter(
        reserva_habitacion__habitacion=habitacion,
        # Condición de solapamiento: 
        # La reserva existente empieza antes de que termine la nueva
        # Y la reserva existente termina después de que empiece la nueva
        fecha_entrada__lt=fecha_salida,
        fecha_salida__gt=fecha_entrada
    )
    
    # Excluir la reserva actual si estamos editando
    if reserva_id:
        reservas_conflictivas = reservas_conflictivas.exclude(id=reserva_id)
    
    disponible = not reservas_conflictivas.exists()
    return disponible, reservas_conflictivas


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
                messages.error(request, 'Debes tener un perfil de cliente para hacer reservas.')
                return redirect('home')
            
            # VALIDAR DISPONIBILIDAD ANTES DE GUARDAR
            disponible, reservas_conflictivas = verificar_disponibilidad(
                habitacion, 
                reserva.fecha_entrada, 
                reserva.fecha_salida
            )
            
            if not disponible:
                # Mostrar mensaje de error con las fechas conflictivas
                conflicto = reservas_conflictivas.first()
                messages.error(
                    request, 
                    f'❌ Lo sentimos, la habitación #{habitacion.numero} no está disponible en las fechas seleccionadas. '
                    f'Ya existe una reserva del {conflicto.fecha_entrada.strftime("%d/%m/%Y")} '
                    f'al {conflicto.fecha_salida.strftime("%d/%m/%Y")}. '
                    f'Por favor, selecciona otras fechas.'
                )
                return render(request, 'hotel/confirmar_reserva.html', {
                    'form': form, 
                    'habitacion': habitacion,
                    'error_disponibilidad': True
                })
            
            reserva.Hotel = habitacion.hotel
            reserva.fecha_reserva = timezone.now().date()
            
            # Calcular monto (días * precio)
            dias = (reserva.fecha_salida - reserva.fecha_entrada).days
            if dias < 1: dias = 1
            reserva.monto = dias * habitacion.precio
            
            reserva.save()
            
            # Crear relación Reserva_Habitacion
            Reserva_Habitacion.objects.create(reserva=reserva, habitacion=habitacion)
            
            # Enviar correo de confirmación
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                hora_reserva = timezone.now().strftime('%H:%M')
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
                    fail_silently=True,
                )
                messages.success(request, f'¡Reserva confirmada exitosamente! Se ha enviado un correo de confirmación a {request.user.email}')
            except Exception as e:
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
            hotel.admin = request.user
            hotel.save()
            messages.success(request, f'Hotel "{hotel.nombre}" creado exitosamente.')
            return redirect('vista_hotel')
    else:
        form = HotelForm()
    
    return render(request, 'hotel/crear_hotel.html', {'form': form})

@login_required
def editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
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
    
    if request.user.rol != 'administrador' or (hotel.admin != request.user and not request.user.is_superuser):
        messages.error(request, 'No tienes permisos para eliminar este hotel.')
        return redirect('vista_hotel')
    
    if request.method == 'POST':
        nombre = hotel.nombre
        hotel.delete()
        messages.success(request, f'Hotel "{nombre}" eliminado exitosamente.')
        return redirect('vista_hotel')
    
    return render(request, 'hotel/eliminar_hotel.html', {'hotel': hotel})