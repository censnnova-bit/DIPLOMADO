from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Salon
from .serializers import SalonSerializer, SalonListSerializer


class SalonViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar salones"""
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'bloque', 'estado', 'tiene_proyector', 'tiene_aire_acondicionado']
    search_fields = ['nombre', 'codigo', 'descripcion']
    ordering_fields = ['nombre', 'capacidad', 'bloque']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SalonListSerializer
        return SalonSerializer
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener solo salones disponibles"""
        salones = self.queryset.filter(estado='disponible')
        serializer = SalonListSerializer(salones, many=True, context={'request': request})
        return Response(serializer.data)
