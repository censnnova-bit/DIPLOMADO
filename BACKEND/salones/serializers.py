from rest_framework import serializers
from .models import Salon


class SalonSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Salon"""
    
    class Meta:
        model = Salon
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class SalonListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de salones"""
    
    class Meta:
        model = Salon
        fields = ['id', 'nombre', 'codigo', 'tipo', 'bloque', 'piso', 'capacidad', 
                  'tiene_proyector', 'tiene_aire_acondicionado', 'estado', 'imagen_url']
