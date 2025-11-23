import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Talkmania.settings')
django.setup()

from talkmaniaApp.models import Hotel, Habitacion, Admin
from django.contrib.auth import get_user_model

User = get_user_model()

def seed():
    # Check if we have any users, if not create a superuser
    if not User.objects.exists():
        print("Creating superuser...")
        user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    else:
        user = User.objects.first()
        print(f"Using existing user: {user.username}")
        
    # Check/Create Admin profile
    # Try to get admin by user first
    try:
        admin_profile = Admin.objects.get(user=user)
        print("Found existing Admin profile for user.")
    except Admin.DoesNotExist:
        print("Creating new Admin profile...")
        admin_profile = Admin.objects.create(
            user=user,
            usuario='admin',
            contraseña='password',
            email='admin@talkmania.com',
            nombre='Admin Principal',
            fecha_creacion='2023-01-01',
            ultimo_acceso='2023-01-01',
            estado=True
        )

    # Create Hotel
    hotel, created = Hotel.objects.get_or_create(
        nombre='Hotel Casino Talca',
        defaults={
            'direccion': 'Av. Circunvalación Ote. 1055, Talca',
            'telefono': '912345678',
            'email': 'contacto@hotelcasino.cl',
            'estrellas': 5,
            'descripcion': 'El mejor hotel de la región del Maule.',
            'estado': True,
            'admin': admin_profile
        }
    )
    
    if created:
        print(f"Created Hotel: {hotel.nombre}")
    else:
        print(f"Hotel already exists: {hotel.nombre}")

    # Create Rooms
    tipos = ['S', 'D', 'SU', 'F']
    precios = {'S': 50000, 'D': 80000, 'SU': 150000, 'F': 120000}
    
    if Habitacion.objects.filter(hotel=hotel).count() < 10:
        print("Creating rooms...")
        for i in range(101, 111): # 10 rooms
            tipo = random.choice(tipos)
            Habitacion.objects.create(
                numero=i,
                tipo=tipo,
                precio=precios[tipo],
                estado='D', # Disponible
                hotel=hotel
            )
        print("Rooms created.")
    else:
        print("Rooms already exist.")

if __name__ == '__main__':
    seed()
