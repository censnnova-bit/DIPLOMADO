from django.db import models
from django.conf import settings
from salones.models import Salon


class Reserva(models.Model):
    """Modelo de reserva de salón"""
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    )
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='reservas')
    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    motivo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    numero_asistentes = models.IntegerField()
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha', '-hora_inicio']
        # Evitar reservas duplicadas en el mismo horario
        unique_together = ['salon', 'fecha', 'hora_inicio']
    
    def __str__(self):
        return f"{self.salon.nombre} - {self.fecha} {self.hora_inicio} ({self.usuario.get_full_name()})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar que hora_fin sea mayor que hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError('La hora de fin debe ser mayor que la hora de inicio')
        
        # Validar que el número de asistentes no exceda la capacidad del salón
        if self.numero_asistentes > self.salon.capacidad:
            raise ValidationError(f'El número de asistentes ({self.numero_asistentes}) excede la capacidad del salón ({self.salon.capacidad})')
