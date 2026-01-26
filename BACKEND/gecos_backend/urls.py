"""
URL configuration for gecos_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from salones.views import SalonViewSet
from reservas.views import ReservaViewSet, AsignaturaViewSet
from usuarios.views import UsuarioViewSet, login_view, logout_view

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="GECOS API",
        default_version='v1',
        description="API para el Sistema de Gestión y Control de Salones (GECOS)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@gecos.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router centralizado
router = DefaultRouter()
router.register(r'salones', SalonViewSet, basename='salon')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'asignaturas', AsignaturaViewSet, basename='asignatura')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    
    # Swagger/OpenAPI URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
