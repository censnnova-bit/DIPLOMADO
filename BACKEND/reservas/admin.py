from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['salon', 'usuario', 'fecha', 'hora_inicio', 'hora_fin', 'estado', 'numero_asistentes']
    list_filter = ['estado', 'fecha', 'salon']
    search_fields = ['salon__nombre', 'usuario__username', 'motivo']
    list_editable = ['estado']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de Reserva', {
            'fields': ('usuario', 'salon', 'fecha', 'hora_inicio', 'hora_fin')
        }),
        ('Detalles', {
            'fields': ('motivo', 'descripcion', 'numero_asistentes')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
