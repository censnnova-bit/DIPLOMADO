from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, LoginSerializer


class IsAdmin(IsAuthenticated):
    """Permiso personalizado para verificar si el usuario es administrador"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.rol == 'admin'


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """Permisos personalizados según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def crear_docente(self, request):
        """Endpoint para que el admin cree usuarios docentes"""
        data = request.data.copy()
        data['rol'] = 'docente'  # Forzar rol docente
        
        serializer = UsuarioCreateSerializer(data=data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                UsuarioSerializer(usuario).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Vista para login que devuelve token"""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    print(f"DEBUG LOGIN: Intentando login con user='{username}' pass='{password}'")
    
    user = authenticate(username=username, password=password)
    
    if not user:
        # Debugging extra
        try:
            u = Usuario.objects.get(username=username)
            print(f"DEBUG LOGIN: Usuario encontrado. pass_valid={u.check_password(password)}")
            print(f"DEBUG LOGIN: is_active={u.is_active}")
        except Usuario.DoesNotExist:
            print(f"DEBUG LOGIN: Usuario '{username}' NO encontrado en DB.")
            
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UsuarioSerializer(user).data
        })
    else:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Vista para logout que elimina el token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Sesión cerrada exitosamente'})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
