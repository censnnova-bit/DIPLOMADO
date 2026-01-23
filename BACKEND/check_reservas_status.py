
import os
import django
import sys

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
django.setup()

from reservas.models import Reserva

print("Reservas existentes:")
for r in Reserva.objects.all():
    print(f"ID: {r.id}, Salon: {r.salon.nombre}, Fecha: {r.fecha}, Estado: '{r.estado}'")
    
print("\nOpciones de estado:")
print(Reserva.ESTADOS)
