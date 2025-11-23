from django.db import models

class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=9)  # ✅ Cambié IntegerField por CharField
    email = models.CharField(max_length=150)
    estrellas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # ✅ Cambié rango a 1-5
    descripcion = models.TextField()
    estado = models.BooleanField()
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.estrellas} estrellas)"

class Habitacion(models.Model):
    TIPOS_HABITACION = [
        ('S', 'Simple'),
        ('D', 'Doble'),
        ('SU', 'Suite'),
        ('F', 'Familiar'),
    ]
    ESTADOS_HABITACION = [
        ('D', 'Disponible'),
        ('O', 'Ocupada'),
        ('M', 'Mantenimiento'),
        ('R', 'Reservada'),
    ]
    
    numero = models.IntegerField()
    tipo = models.CharField(max_length=2, choices=TIPOS_HABITACION) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=1, choices=ESTADOS_HABITACION, default='D')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')

    def __str__(self):
        return f'Habitación {self.numero} - {self.hotel.nombre}'

class Review(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reserva = models.ForeignKey('HotelesApp.Reserva', on_delete=models.CASCADE, related_name='reviews')
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'reserva']
    
    def __str__(self):
        return f"Review de {self.usuario.username} - {self.calificacion}★"