from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Modelo de usuario extendido"""
    ROLES = (
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='docente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"
