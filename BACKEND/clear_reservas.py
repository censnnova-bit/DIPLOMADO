
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
django.setup()

from reservas.models import Reserva

print(f"Borrando {Reserva.objects.count()} reservas existentes...")
Reserva.objects.all().delete()
print("Todas las reservas han sido eliminadas.")
