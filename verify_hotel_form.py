import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Talkmania.settings')
django.setup()

from talkmaniaApp.forms import HotelForm

form = HotelForm()
print("HotelForm instantiated successfully.")
print(form.as_p())
