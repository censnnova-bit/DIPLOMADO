#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gecos_backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth import get_user_model
from salones.models import Salon

Usuario = get_user_model()

print('Poblando base de datos...\n')

# Crear usuarios
print('Creando usuarios...')

# Admin
admin, created = Usuario.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@fesc.edu.co',
        'first_name': 'Administrador',
        'last_name': 'Sistema',
        'rol': 'admin',
        'documento': '1000000001',
        'telefono': '3001234567',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin.set_password('Admin123!')
    admin.save()
    print('✅ Usuario admin creado')
else:
    print('ℹ️  Usuario admin ya existe')

# Docente 1
docente, created = Usuario.objects.get_or_create(
    username='docente1',
    defaults={
        'email': 'docente1@fesc.edu.co',
        'first_name': 'Carlos',
        'last_name': 'Martínez',
        'rol': 'docente',
        'documento': '1000000002',
        'telefono': '3009876543',
    }
)
if created:
    docente.set_password('Docente123!')
    docente.save()
    print('✅ Usuario docente1 creado')
else:
    print('ℹ️  Usuario docente1 ya existe')

# Docente 2
docente2, created = Usuario.objects.get_or_create(
    username='docente2',
    defaults={
        'email': 'docente2@fesc.edu.co',
        'first_name': 'María',
        'last_name': 'González',
        'rol': 'docente',
        'documento': '1000000003',
        'telefono': '3005551234',
    }
)
if created:
    docente2.set_password('Docente123!')
    docente2.save()
    print('✅ Usuario docente2 creado')
else:
    print('ℹ️  Usuario docente2 ya existe')

# Crear salones
print('\nCreando salones...')

salones_data = [
    {
        'nombre': 'Aula A-204',
        'codigo': 'A204',
        'tipo': 'aula',
        'bloque': 'Bloque A',
        'piso': '2º Piso',
        'capacidad': 30,
        'descripcion': 'Aula estándar para clases magistrales',
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500&q=80'
    },
    {
        'nombre': 'Lab. Informática 1',
        'codigo': 'LAB301',
        'tipo': 'laboratorio',
        'bloque': 'Bloque B',
        'piso': '3º Piso',
        'capacidad': 25,
        'descripcion': 'Laboratorio de computación con 25 equipos',
        'tiene_computadores': True,
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500&q=80'
    },
    {
        'nombre': 'Auditorio Magna',
        'codigo': 'AUD01',
        'tipo': 'auditorio',
        'bloque': 'Planta Baja',
        'piso': 'PB',
        'capacidad': 120,
        'descripcion': 'Auditorio principal para eventos y conferencias',
        'tiene_proyector': True,
        'tiene_smart_tv': True,
        'tiene_audio': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80'
    },
    {
        'nombre': 'Sala de Conferencias 1',
        'codigo': 'CONF401',
        'tipo': 'sala_conferencias',
        'bloque': 'Bloque C',
        'piso': '4º Piso',
        'capacidad': 15,
        'descripcion': 'Sala para reuniones y conferencias pequeñas',
        'tiene_smart_tv': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=500&q=80'
    },
    {
        'nombre': 'Aula B-105',
        'codigo': 'B105',
        'tipo': 'aula',
        'bloque': 'Bloque B',
        'piso': '1º Piso',
        'capacidad': 40,
        'descripcion': 'Aula amplia con capacidad para 40 estudiantes',
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1562774053-701939374585?w=500&q=80'
    },
    {
        'nombre': 'Lab. Física',
        'codigo': 'LAB201',
        'tipo': 'laboratorio',
        'bloque': 'Bloque A',
        'piso': '2º Piso',
        'capacidad': 20,
        'descripcion': 'Laboratorio equipado para prácticas de física',
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=500&q=80'
    },
    {
        'nombre': 'Aula C-302',
        'codigo': 'C302',
        'tipo': 'aula',
        'bloque': 'Bloque C',
        'piso': '3º Piso',
        'capacidad': 35,
        'descripcion': 'Aula moderna con tecnología audiovisual',
        'tiene_proyector': True,
        'tiene_smart_tv': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=500&q=80'
    },
    {
        'nombre': 'Lab. Química',
        'codigo': 'LAB202',
        'tipo': 'laboratorio',
        'bloque': 'Bloque A',
        'piso': '2º Piso',
        'capacidad': 18,
        'descripcion': 'Laboratorio especializado en química',
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'mantenimiento',
        'imagen_url': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=500&q=80'
    },
    {
        'nombre': 'Aula D-101',
        'codigo': 'D101',
        'tipo': 'aula',
        'bloque': 'Bloque D',
        'piso': '1º Piso',
        'capacidad': 50,
        'descripcion': 'Aula grande para clases numerosas',
        'tiene_proyector': True,
        'tiene_aire_acondicionado': True,
        'tiene_audio': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=500&q=80'
    },
    {
        'nombre': 'Sala Multimedia',
        'codigo': 'MULT501',
        'tipo': 'sala_conferencias',
        'bloque': 'Bloque C',
        'piso': '5º Piso',
        'capacidad': 25,
        'descripcion': 'Sala equipada con tecnología multimedia avanzada',
        'tiene_proyector': True,
        'tiene_smart_tv': True,
        'tiene_audio': True,
        'tiene_aire_acondicionado': True,
        'tiene_wifi': True,
        'estado': 'disponible',
        'imagen_url': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=500&q=80'
    },
]

salones_creados = 0
for salon_data in salones_data:
    salon, created = Salon.objects.get_or_create(
        codigo=salon_data['codigo'],
        defaults=salon_data
    )
    if created:
        salones_creados += 1
        print(f'✅ Salón {salon.nombre} creado')
    else:
        print(f'ℹ️  Salón {salon.nombre} ya existe')

print(f'\n✅ Base de datos poblada exitosamente!')
print(f'📊 Total: {salones_creados} salones nuevos creados')
print(f'📊 Total en BD: {Salon.objects.count()} salones, {Usuario.objects.count()} usuarios')

# Mostrar credenciales
print('\n' + '='*60)
print('🔑 CREDENCIALES DE ACCESO')
print('='*60)
print('\n1. Administrador:')
print('   Usuario: admin')
print('   Contraseña: Admin123!')
print('\n2. Docente:')
print('   Usuario: docente1')
print('   Contraseña: Docente123!')
print('\n' + '='*60)
