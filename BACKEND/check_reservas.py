
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
django.setup()

from reservas.models import Reserva
from django.utils import timezone

print(f"Timezone actual: {timezone.get_current_timezone_name()}")
print(f"Fecha/Hora actual (timezone): {timezone.localtime(timezone.now())}")
print(f"Fecha actual (today): {timezone.localdate()}")

reservas = Reserva.objects.all().order_by('-fecha')
print(f"\nTotal reservas: {reservas.count()}")
for r in reservas[:5]:
    print(f"Reserva: {r.id} | Fecha: {r.fecha} | Salon: {r.salon.nombre} | Usuario: {r.usuario.username}")
