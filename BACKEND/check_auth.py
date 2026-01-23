import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth import authenticate

user = authenticate(username='admin', password='Admin123!')
if user:
    print("✅ Autenticación exitosa en el Backend.")
else:
    print("❌ Falló la autenticación en el Backend. Contraseña incorrecta.")
