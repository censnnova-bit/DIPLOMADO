from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 
                  'telefono', 'documento', 'fecha_creacion', 'is_active']
        read_only_fields = ['id', 'fecha_creacion']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios con contraseña"""
    password = serializers.CharField(write_only=True, required=True, min_length=6, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 
                  'rol', 'telefono', 'documento']
        extra_kwargs = {
            'email': {'required': False},
            'telefono': {'required': False},
            'documento': {'required': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
