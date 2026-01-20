from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from salones.models import Salon
from reservas.models import Reserva
from datetime import datetime, date, timedelta

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos iniciales para testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Poblando base de datos...')
        
        # Crear usuarios
        self.stdout.write('Creando usuarios...')
        
        # Admin
        admin, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@gecos.com',
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
            self.stdout.write(self.style.SUCCESS(f'✅ Usuario admin creado'))
        
        # Docente
        docente, created = Usuario.objects.get_or_create(
            username='docente1',
            defaults={
                'email': 'docente1@gecos.com',
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
            self.stdout.write(self.style.SUCCESS(f'✅ Usuario docente1 creado'))
        
        # Estudiante
        estudiante, created = Usuario.objects.get_or_create(
            username='estudiante1',
            defaults={
                'email': 'estudiante1@gecos.com',
                'first_name': 'Ana',
                'last_name': 'García',
                'rol': 'estudiante',
                'documento': '1000000003',
                'telefono': '3005551234',
            }
        )
        if created:
            estudiante.set_password('Estudiante123!')
            estudiante.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Usuario estudiante1 creado'))
        
        # Crear salones
        self.stdout.write('Creando salones...')
        
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
        
        salones_creados = []
        for salon_data in salones_data:
            salon, created = Salon.objects.get_or_create(
                codigo=salon_data['codigo'],
                defaults=salon_data
            )
            if created:
                salones_creados.append(salon)
                self.stdout.write(self.style.SUCCESS(f'✅ Salón {salon.nombre} creado'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Base de datos poblada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total: {len(salones_creados)} salones creados'))
        
        # Mostrar credenciales
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🔑 CREDENCIALES DE ACCESO'))
        self.stdout.write('='*60)
        self.stdout.write(f'\n1. Administrador:')
        self.stdout.write(f'   Usuario: admin')
        self.stdout.write(f'   Contraseña: Admin123!')
        self.stdout.write(f'\n2. Docente:')
        self.stdout.write(f'   Usuario: docente1')
        self.stdout.write(f'   Contraseña: Docente123!')
        self.stdout.write(f'\n3. Estudiante:')
        self.stdout.write(f'   Usuario: estudiante1')
        self.stdout.write(f'   Contraseña: Estudiante123!')
        self.stdout.write('\n' + '='*60 + '\n')
