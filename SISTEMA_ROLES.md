# Sistema de Roles - Administración y Docentes

## Cambios Implementados

### 1. Backend - Modelo de Usuarios

**Archivo**: `usuarios/models.py`
- ✅ Actualizado el modelo `Usuario` para incluir solo dos roles:
  - `admin` (Administrador)
  - `docente` (Docente)
- ✅ Eliminado el rol `estudiante`
- ✅ Valor por defecto cambiado de `estudiante` a `docente`
- ✅ Migración creada: `0002_alter_usuario_rol.py`

### 2. Backend - Serializers de Reservas

**Archivo**: `reservas/serializers.py`
- ✅ Agregado campo `usuario_nombre` al `ReservaSerializer`
- ✅ Este campo muestra el nombre completo del usuario que creó la reserva

### 3. Frontend - Nuevas Vistas de Administración

#### AdminSalones.vue
**Funcionalidades**:
- ✅ Vista completa CRUD de salones (Crear, Leer, Actualizar, Eliminar)
- ✅ Tabla con listado de todos los salones
- ✅ Modal para crear/editar salones con todos los campos:
  - Información básica (nombre, código, tipo, estado)
  - Ubicación (bloque, piso)
  - Capacidad y descripción
  - Equipamiento (proyector, aire, computadores, TV, audio, WiFi)
  - Imagen URL
- ✅ Filtros visuales por tipo, bloque y estado
- ✅ Confirmación antes de eliminar
- ✅ Protección: Solo usuarios admin pueden acceder

#### AdminReservas.vue
**Funcionalidades**:
- ✅ Vista completa de gestión de reservas
- ✅ Tabla con todas las reservas del sistema
- ✅ Filtro por estado (pendiente, aprobada, rechazada, cancelada, completada)
- ✅ Acciones rápidas:
  - Aprobar reservas pendientes (✓)
  - Rechazar reservas pendientes (✗)
  - Eliminar cualquier reserva (🗑)
- ✅ Información detallada: fecha, horario, salón, motivo, asistentes, usuario
- ✅ Cambio de estado con actualización inmediata
- ✅ Protección: Solo usuarios admin pueden acceder

### 4. Frontend - Componente de Notificaciones

**Archivo**: `components/AdminNotifications.vue`
**Funcionalidades**:
- ✅ Componente que se muestra automáticamente al iniciar sesión como admin
- ✅ Muestra reservas aprobadas del día actual
- ✅ Lista de salones ocupados con:
  - Motivo de la reserva
  - Horario (inicio - fin)
  - Nombre del usuario
- ✅ Link directo a "Gestionar Reservas"
- ✅ Animación de entrada (slide-in)
- ✅ Botón para cerrar notificaciones

### 5. Frontend - Navegación por Rol

**Archivo**: `components/Header.vue`
**Cambios**:
- ✅ Menú dinámico basado en el rol del usuario
- ✅ **Para Admin**:
  - Salones (vista general)
  - Gestionar Salones (CRUD)
  - Gestionar Reservas (aprobación/rechazo)
- ✅ **Para Docente**:
  - Salones (vista general)
  - Mis Reservas (solo sus reservas)
- ✅ Indicador visual del rol en el header

### 6. Frontend - Router y Protección de Rutas

**Archivo**: `router/index.js`
**Cambios**:
- ✅ Nuevas rutas agregadas:
  - `/admin/salones` - Vista AdminSalones
  - `/admin/reservas` - Vista AdminReservas
- ✅ Protección de rutas admin con `requiresAdmin: true`
- ✅ Guard de navegación que redirige a `/salones` si un no-admin intenta acceder a rutas protegidas

### 7. Frontend - API Service

**Archivo**: `services/api.js`
**Nuevos endpoints**:
- ✅ `createSalon(data)` - Crear nuevo salón
- ✅ `updateSalon(id, data)` - Actualizar salón existente
- ✅ `deleteSalon(id)` - Eliminar salón
- ✅ `updateReserva(id, data)` - Actualizar estado de reserva

### 8. Frontend - Store de Autenticación

**Archivo**: `stores/auth.js`
**Cambios**:
- ✅ Eliminada propiedad `isEstudiante` (ya no se necesita)
- ✅ Mantiene `isAdmin` e `isDocente` para control de acceso

### 9. Backend - Script de Población

**Archivo**: `poblar_datos.py`
**Cambios**:
- ✅ Eliminado usuario `estudiante1`
- ✅ Agregado segundo docente: `docente2`
- ✅ Usuarios actualizados:
  - `admin` - Administrador Sistema
  - `docente1` - Carlos Martínez
  - `docente2` - María González

## Credenciales de Acceso

### Administrador
- **Usuario**: `admin`
- **Contraseña**: `Admin123!`
- **Rol**: admin
- **Acceso**: Todas las funcionalidades + gestión completa

### Docente 1
- **Usuario**: `docente1`
- **Contraseña**: `Docente123!`
- **Rol**: docente
- **Acceso**: Ver salones y gestionar sus propias reservas

### Docente 2
- **Usuario**: `docente2`
- **Contraseña**: `Docente123!`
- **Rol**: docente
- **Acceso**: Ver salones y gestionar sus propias reservas

## Pasos para Aplicar Cambios

### 1. Aplicar Migración de Base de Datos
```bash
cd BACKEND
python manage.py migrate
```

### 2. Poblar Datos Actualizados
```bash
python poblar_datos.py
```

### 3. Reiniciar Servidor (si no se reinició automáticamente)
```bash
# El servidor debe detectar cambios automáticamente
# Si es necesario reiniciar manualmente:
Ctrl+C
python manage.py runserver
```

### 4. Probar en el Frontend
1. Acceder a http://localhost:5173/login
2. Iniciar sesión como `admin` / `Admin123!`
3. Verificar que aparezcan las opciones:
   - Gestionar Salones
   - Gestionar Reservas
4. Verificar notificaciones de salones ocupados
5. Probar CRUD de salones
6. Probar aprobación/rechazo de reservas

## Flujo de Trabajo Admin

### Gestión de Salones
1. Click en "Gestionar Salones"
2. Ver tabla de salones existentes
3. Click en "Nuevo Salón" para crear
4. Click en "Editar" para modificar
5. Click en "Eliminar" para borrar (con confirmación)

### Gestión de Reservas
1. Click en "Gestionar Reservas"
2. Ver todas las reservas del sistema
3. Filtrar por estado si es necesario
4. Para reservas pendientes:
   - Click en ✓ para aprobar
   - Click en ✗ para rechazar
5. Click en 🗑 para eliminar cualquier reserva

### Notificaciones
- Aparecen automáticamente al iniciar sesión
- Muestran reservas activas del día
- Se pueden cerrar con el botón X
- Link directo a gestión de reservas

## Arquitectura de Permisos

### Nivel de Vista (Frontend)
- Header muestra opciones según `authStore.isAdmin`
- Componentes admin verifican rol al montarse
- Redirigen a `/salones` si el usuario no es admin

### Nivel de Router
- Meta field `requiresAdmin: true`
- beforeEach guard verifica `authStore.isAdmin`
- Redirige automáticamente si falta permiso

### Nivel de Backend (Pendiente para Producción)
- Actualmente: `permission_classes = [AllowAny]` para desarrollo
- **Recomendado para producción**:
  - Cambiar a `IsAuthenticated` en todos los viewsets
  - Agregar `IsAdminUser` para operaciones destructivas
  - Implementar permisos personalizados por rol

## Próximos Pasos Sugeridos

### Seguridad
1. ⚠️ Cambiar `AllowAny` a `IsAuthenticated` en producción
2. Implementar permisos a nivel de ViewSet
3. Agregar throttling para prevenir abuso

### Funcionalidades Adicionales
1. Historial de cambios en salones
2. Exportación de reportes (Excel/PDF)
3. Estadísticas de ocupación
4. Sistema de aprobación automática basado en reglas
5. Notificaciones por email

### UX Mejoras
1. Toast notifications en lugar de alert()
2. Loading states más refinados
3. Búsqueda avanzada en tablas
4. Paginación en vista de reservas
5. Bulk actions (aprobar múltiples, etc.)

## Archivos Modificados/Creados

### Backend
- ✅ `usuarios/models.py` - Modelo actualizado
- ✅ `usuarios/migrations/0002_alter_usuario_rol.py` - Nueva migración
- ✅ `reservas/serializers.py` - Campo usuario_nombre agregado
- ✅ `poblar_datos.py` - Script actualizado

### Frontend
- ✅ `views/AdminSalones.vue` - Nueva vista
- ✅ `views/AdminReservas.vue` - Nueva vista
- ✅ `components/AdminNotifications.vue` - Nuevo componente
- ✅ `components/Header.vue` - Navegación dinámica
- ✅ `views/ClassroomList.vue` - Integración de notificaciones
- ✅ `services/api.js` - Nuevos endpoints
- ✅ `router/index.js` - Rutas y guards
- ✅ `stores/auth.js` - Eliminado isEstudiante

## Validación de Implementación

### Checklist de Pruebas
- [ ] Login como admin funciona
- [ ] Login como docente funciona
- [ ] Admin ve "Gestionar Salones" en menú
- [ ] Admin ve "Gestionar Reservas" en menú
- [ ] Docente NO ve opciones de gestión
- [ ] Docente ve "Mis Reservas"
- [ ] Notificaciones aparecen para admin
- [ ] CRUD de salones funciona (crear, editar, eliminar)
- [ ] Aprobación de reservas funciona
- [ ] Rechazo de reservas funciona
- [ ] Eliminación de reservas funciona
- [ ] Filtros de reservas funcionan
- [ ] Protección de rutas funciona (docente no accede a /admin/*)
- [ ] Migración aplicada sin errores
- [ ] Datos poblados correctamente

---

**Fecha**: 19 de Enero de 2026
**Versión**: 2.0
**Estado**: ✅ Implementado
