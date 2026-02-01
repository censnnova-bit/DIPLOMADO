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
    status = serializers.SerializerMethodField()
    statusText = serializers.SerializerMethodField()
    statusColor = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = Salon
        fields = ['id', 'nombre', 'codigo', 'tipo', 'bloque', 'piso', 'capacidad', 
                  'tiene_proyector', 'tiene_aire_acondicionado', 'estado', 'imagen_url', 'imagen',
                  'status', 'statusText', 'statusColor', 'features', 'schedule']

    def get_status(self, obj):
        mapping = {
            'disponible': 'available',
            'ocupado': 'occupied',
            'mantenimiento': 'maintenance'
        }
        return mapping.get(obj.estado, 'available')

    def get_statusText(self, obj):
         return obj.get_estado_display()

    def get_statusColor(self, obj):
        colors = {
            'disponible': '#22c55e', # green-500
            'ocupado': '#ef4444',    # red-500
            'mantenimiento': '#f97316' # orange-500
        }
        return colors.get(obj.estado, '#cccccc')

    def get_features(self, obj):
        feats = []
        if obj.tiene_proyector:
            feats.append({
                'name': 'Proyector', 
                'icon': 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z'
            })
        if obj.tiene_aire_acondicionado:
            feats.append({
                'name': 'Aire Acondicionado', 
                'icon': 'M12 12c0-3 2.5-6 2.5-6s2.5 3 2.5 6-2.5 6-2.5 6-2.5-3-2.5-6zm0 0c0 3-2.5 6-2.5 6s-2.5-3-2.5-6 2.5-6 2.5-6 2.5 3 2.5 6zm0 0c3 0 6-2.5 6-2.5s-3-2.5-6-2.5-6 2.5-6 2.5 3 2.5 6 2.5zm0 0c-3 0-6 2.5-6 2.5s3 2.5 6 2.5 6-2.5 6-2.5-3-2.5-6-2.5z'
            })
        if obj.tiene_computadores:
             feats.append({
                'name': 'Computadores', 
                'icon': 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
            })
        if obj.tiene_wifi:
             feats.append({
                'name': 'WiFi', 
                'icon': 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0'
            })
        return feats

    def get_schedule(self, obj):
        from datetime import datetime, time, timedelta
        from django.utils import timezone
        # Importación dentro del método para evitar ciclos
        from reservas.models import Reserva
        
        # Intentar obtener la fecha del query param, si no existe usar hoy (local)
        request = self.context.get('request')
        # Usar .GET en lugar de .query_params para compatibilidad con requests de Django puro y DRF
        fecha_param = request.GET.get('fecha') if request else None
        
        if fecha_param:
            try:
                today = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except ValueError:
                local_now = timezone.localtime(timezone.now())
                today = local_now.date()
        else:
            local_now = timezone.localtime(timezone.now())
            today = local_now.date()
        
        # DEBUG: Imprimir para verificar qué fecha se está consultando realmente
        # print(f"DEBUG: Salon {obj.codigo} - Consultando fecha: {today}")

        # Definir horario de operación extendido (6 AM - 10 PM)
        start_hour = 6
        end_hour = 22
        slots = []
        
        # Filtrar reservas confirmadas para este salón y esta fecha
        reservations = Reserva.objects.filter(
            salon=obj, 
            fecha=today,
            estado__in=['confirmada', 'completada', 'pendiente']
        )
        
        for h in range(start_hour, end_hour):
            slot_start = time(h, 0)
            slot_end = time(h + 1, 0)
            
            status = 'available'
            
            # Verificar si hay reserva en este bloque
            for res in reservations:
                # Lógica de intersección de rangos:
                # Un intervalo [A, B] se solapa con [C, D] si A < D y B > C
                if (res.hora_inicio < slot_end) and (res.hora_fin > slot_start):
                    status = 'occupied'
                    break
            
            slots.append({
                'time': f"{h:02d}:00",
                'status': status
            })
            
        return slots
