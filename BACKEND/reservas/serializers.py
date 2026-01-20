from rest_framework import serializers
from .models import Reserva
from salones.serializers import SalonListSerializer
from usuarios.serializers import UsuarioSerializer


class ReservaSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Reserva"""
    salon_detalle = SalonListSerializer(source='salon', read_only=True)
    usuario_detalle = UsuarioSerializer(source='usuario', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'usuario_detalle', 'usuario_nombre', 'salon', 'salon_detalle', 
                  'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'descripcion', 
                  'numero_asistentes', 'estado', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate(self, attrs):
        # Validar que hora_fin sea mayor que hora_inicio
        if attrs.get('hora_fin') and attrs.get('hora_inicio'):
            if attrs['hora_fin'] <= attrs['hora_inicio']:
                raise serializers.ValidationError(
                    {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
                )
        
        # Validar capacidad
        if attrs.get('salon') and attrs.get('numero_asistentes'):
            if attrs['numero_asistentes'] > attrs['salon'].capacidad:
                raise serializers.ValidationError(
                    {"numero_asistentes": f"El número de asistentes excede la capacidad del salón ({attrs['salon'].capacidad})"}
                )
        
        return attrs


class ReservaCreateSerializer(serializers.ModelSerializer):
    """Serializer simplificado para crear reservas"""
    
    class Meta:
        model = Reserva
        fields = ['salon', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 
                  'descripcion', 'numero_asistentes']
    
    def validate(self, attrs):
        # Validar que hora_fin sea mayor que hora_inicio
        if attrs['hora_fin'] <= attrs['hora_inicio']:
            raise serializers.ValidationError(
                {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
            )
        
        # Validar capacidad
        if attrs['numero_asistentes'] > attrs['salon'].capacidad:
            raise serializers.ValidationError(
                {"numero_asistentes": f"El número de asistentes excede la capacidad del salón ({attrs['salon'].capacidad})"}
            )
        
        return attrs
