from django.db import models

class Reserva(models.Model):
    cliente = models.ForeignKey('usuarios.Cliente', on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reserva {self.id} - {self.cliente}"
