from django.contrib import admin
from .models import Hotel, Habitacion, Reserva, Cliente, Admin, tipo_pago

# Register your models here.
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'estrellas', 'estado')
    search_fields = ('nombre', 'direccion')
    list_filter = ('estrellas', 'estado')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'hotel', 'tipo', 'precio', 'estado')
    list_filter = ('hotel', 'tipo', 'estado')
    search_fields = ('numero', 'hotel__nombre')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cliente', 'Hotel', 'fecha_entrada', 'fecha_salida', 'estado', 'monto')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = ('Cliente__nombre', 'Hotel__nombre')

admin.site.register(Cliente)
admin.site.register(Admin)
admin.site.register(tipo_pago)
