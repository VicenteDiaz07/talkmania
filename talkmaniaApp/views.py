from django.shortcuts import render
from .models import *

# Create your views here.
def vista_hotel(request):
    hoteles = Hotel.objects.all()
    return render(request, 'hotel/hoteles.html', {'hoteles': hoteles})

    