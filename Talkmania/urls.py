
"""
URL configuration for Talkmania project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import index
from talkmaniaApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro_exotico/', index, name='index'), 
    path('usuarios/', include('usuarios.urls')),
    path('', vista_hotel, name='vista_hotel'),
    path('hoteles/<int:hotel_id>/', vista_detalle_hotel, name='detalle_hotel'),
    path('hoteles/crear/', crear_hotel, name='crear_hotel'),
    path('hoteles/editar/<int:hotel_id>/', editar_hotel, name='editar_hotel'),
    path('hoteles/eliminar/<int:hotel_id>/', eliminar_hotel, name='eliminar_hotel'),
    path('hoteles/agregar-habitacion/', agregar_habitacion, name='agregar_habitacion'),
    path('hoteles/reservar/<int:habitacion_id>/', confirmar_reserva, name='confirmar_reserva'),
]