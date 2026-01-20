from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Reserva
from .serializers import ReservaSerializer, ReservaCreateSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar reservas"""
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [AllowAny]  # Temporalmente permitir acceso sin autenticación
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salon', 'fecha', 'estado', 'usuario']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservaCreateSerializer
        return ReservaSerializer
    
    def perform_create(self, serializer):
        """Asignar el usuario actual a la reserva, o crear un usuario temporal si no está autenticado"""
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            # Para pruebas: usar el primer usuario disponible
            from usuarios.models import Usuario
            usuario = Usuario.objects.first()
            if usuario:
                serializer.save(usuario=usuario)
            else:
                # Crear un usuario temporal si no existe ninguno
                usuario = Usuario.objects.create_user(
                    email='usuario@demo.com',
                    nombre='Usuario Demo',
                    password='demo123'
                )
                serializer.save(usuario=usuario)
    
    @action(detail=False, methods=['get'])
    def mis_reservas(self, request):
        """Obtener reservas del usuario actual"""
        reservas = self.queryset.filter(usuario=request.user)
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancelar una reserva"""
        reserva = self.get_object()
        
        # Solo el usuario que creó la reserva puede cancelarla
        if reserva.usuario != request.user and not request.user.is_staff:
            return Response(
                {'error': 'No tienes permiso para cancelar esta reserva'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reserva.estado = 'cancelada'
        reserva.save()
        
        serializer = self.get_serializer(reserva)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        """Confirmar una reserva (solo admin)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo administradores pueden confirmar reservas'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reserva = self.get_object()
        reserva.estado = 'confirmada'
        reserva.save()
        
        serializer = self.get_serializer(reserva)
        return Response(serializer.data)
