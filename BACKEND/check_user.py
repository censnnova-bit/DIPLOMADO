import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth import get_user_model
Usuario = get_user_model()

try:
    admin = Usuario.objects.get(username='admin')
    print(f"✅ Usuario 'admin' encontrado. ID: {admin.id}, Rol: {getattr(admin, 'rol', 'N/A')}")
    print("Intenta loguearte con: admin / Admin123!")
except Usuario.DoesNotExist:
    print("❌ El usuario 'admin' NO existe en la base de datos.")
    print("Por favor ejecuta: python manage.py migrate && python poblar_datos.py")
except Exception as e:
    print(f"Error al consultar la base de datos: {e}")
