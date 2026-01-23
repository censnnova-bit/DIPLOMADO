from rest_framework import serializers
from .models import Reserva, Asignatura
from salones.serializers import SalonListSerializer
from usuarios.serializers import UsuarioSerializer


class AsignaturaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asignatura"""
    class Meta:
        model = Asignatura
        fields = '__all__'
        read_only_fields = ['codigo']


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
        from django.utils import timezone
        
        # Validar que hora_fin sea mayor que hora_inicio
        if attrs.get('hora_fin') and attrs.get('hora_inicio'):
            if attrs['hora_fin'] <= attrs['hora_inicio']:
                raise serializers.ValidationError(
                    {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
                )
        
        # Validar fechas pasadas
        if attrs.get('fecha'):
            now = timezone.localtime(timezone.now())
            hoy = now.date()
            if attrs['fecha'] < hoy:
                raise serializers.ValidationError(
                    {"fecha": "No se pueden crear reservas en fechas pasadas."}
                )
            
            # Si es hoy, validar hora
            if attrs['fecha'] == hoy and attrs.get('hora_inicio'):
                if attrs['hora_inicio'] < now.time():
                    raise serializers.ValidationError(
                        {"hora_inicio": "No se puede reservar en una hora que ya ha pasado."}
                    )
        
        # Validar capacidad
        if attrs.get('salon') and attrs.get('numero_asistentes'):
            if attrs['numero_asistentes'] > attrs['salon'].capacidad:
                raise serializers.ValidationError(
                    {"numero_asistentes": f"El número de asistentes excede la capacidad del salón ({attrs['salon'].capacidad})"}
                )

        # Validar solapamiento de horarios (Overlap)
        if attrs.get('salon') and attrs.get('fecha') and attrs.get('hora_inicio') and attrs.get('hora_fin'):
            salon = attrs['salon']
            fecha = attrs['fecha']
            inicio = attrs['hora_inicio']
            fin = attrs['hora_fin']
            
            # Buscar reservas existentes que se solapen
            # (StartA < EndB) and (EndA > StartB)
            solapamientos = Reserva.objects.filter(
                salon=salon,
                fecha=fecha,
                estado__in=['pendiente', 'confirmada', 'completada']
            ).exclude(
                id=self.instance.id if self.instance else None
            ).filter(
                hora_inicio__lt=fin,
                hora_fin__gt=inicio
            )
            
            if solapamientos.exists():
                raise serializers.ValidationError(
                    {"non_field_errors": ["Ya existe una reserva confirmada o pendiente en este horario para este salón."]}
                )
        
        return attrs


class ReservaCreateSerializer(serializers.ModelSerializer):
    """Serializer simplificado para crear reservas"""
    
    class Meta:
        model = Reserva
        fields = ['salon', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 
                  'descripcion', 'numero_asistentes']
    
    def validate(self, attrs):
        from django.utils import timezone

        # Validar que hora_fin sea mayor que hora_inicio
        if attrs['hora_fin'] <= attrs['hora_inicio']:
            raise serializers.ValidationError(
                {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
            )
            
        # Validar fechas pasadas
        now = timezone.localtime(timezone.now())
        hoy = now.date()
        
        if attrs['fecha'] < hoy:
            raise serializers.ValidationError(
                {"fecha": "No se pueden crear reservas en fechas pasadas."}
            )
            
        # Si es hoy, validar que la hora de inicio no haya pasado
        if attrs['fecha'] == hoy:
            if attrs['hora_inicio'] < now.time():
                 raise serializers.ValidationError(
                    {"hora_inicio": "No se puede reservar en una hora que ya ha pasado."}
                )
        
        # Validar capacidad
        if attrs['numero_asistentes'] > attrs['salon'].capacidad:
            raise serializers.ValidationError(
                {"numero_asistentes": f"El número de asistentes excede la capacidad del salón ({attrs['salon'].capacidad})"}
            )
            
        # Validar solapamiento de horarios (Overlap)
        salon = attrs['salon']
        fecha = attrs['fecha']
        inicio = attrs['hora_inicio']
        fin = attrs['hora_fin']
        
        solapamientos = Reserva.objects.filter(
            salon=salon,
            fecha=fecha,
            estado__in=['pendiente', 'confirmada', 'completada']
        ).filter(
            hora_inicio__lt=fin,
            hora_fin__gt=inicio
        )
        
        if solapamientos.exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["Ya existe una reserva confirmada o pendiente en este horario para este salón."]}
            )
        
        return attrs
