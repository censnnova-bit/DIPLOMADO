from django.contrib import admin
from .models import Salon


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'tipo', 'bloque', 'piso', 'capacidad', 'estado']
    list_filter = ['tipo', 'estado', 'bloque', 'tiene_proyector', 'tiene_aire_acondicionado']
    search_fields = ['nombre', 'codigo', 'descripcion']
    list_editable = ['estado']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'tipo', 'bloque', 'piso', 'capacidad', 'descripcion', 'imagen_url')
        }),
        ('Recursos', {
            'fields': ('tiene_proyector', 'tiene_computadores', 'tiene_aire_acondicionado', 
                      'tiene_smart_tv', 'tiene_audio', 'tiene_wifi')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
