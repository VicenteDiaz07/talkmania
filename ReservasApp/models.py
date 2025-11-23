from django.db import models

# Create your models here.

class Reserva(models.Model):
    cliente = models.ForeignKey('usuarios.Cliente', on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reserva {self.id} - {self.cliente}"

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='pendiente')