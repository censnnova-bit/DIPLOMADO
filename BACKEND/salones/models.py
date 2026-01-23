from django.db import models


class Salon(models.Model):
    """Modelo de salón o aula"""
    ESTADOS = (
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En Mantenimiento'),
    )
    
    TIPOS = (
        ('aula', 'Aula Regular'),
        ('laboratorio', 'Laboratorio'),
        ('auditorio', 'Auditorio'),
        ('sala_conferencias', 'Sala de Conferencias'),
    )
    
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPOS, default='aula')
    bloque = models.CharField(max_length=50)
    piso = models.CharField(max_length=10)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    
    # Recursos disponibles
    tiene_proyector = models.BooleanField(default=False)
    tiene_computadores = models.BooleanField(default=False)
    tiene_aire_acondicionado = models.BooleanField(default=False)
    tiene_smart_tv = models.BooleanField(default=False)
    tiene_audio = models.BooleanField(default=False)
    tiene_wifi = models.BooleanField(default=False)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    imagen_url = models.URLField(blank=True, null=True)
    imagen = models.ImageField(upload_to='salones/', blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Salón'
        verbose_name_plural = 'Salones'
        ordering = ['bloque', 'piso', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.bloque} ({self.capacidad} personas)"
