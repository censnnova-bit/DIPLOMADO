# 🎯 Guía Rápida - Sistema de Roles GECOS

## ✅ Cambios Realizados

He implementado el sistema de roles con **Admin** y **Docente** (sin estudiantes) con todas las funcionalidades solicitadas:

### 🔐 Roles Disponibles

1. **Administrador (Admin)**
   - ✨ Gestionar Salones (crear, editar, eliminar)
   - ✨ Gestionar Reservas (aprobar, rechazar, eliminar)
   - ✨ Ver notificaciones de salones ocupados al iniciar sesión
   - ✨ Acceso completo a todo el sistema

2. **Docente**
   - ✨ Ver y reservar salones
   - ✨ Gestionar sus propias reservas
   - ✨ Ver disponibilidad en tiempo real

## 📋 Pasos para Probar

### 1. Aplicar Cambios en la Base de Datos

Abre una **nueva terminal** y ejecuta:

```bash
cd "c:\Users\wvelasco\OneDrive - Grupo EPM\Documentos\DIPLOMADO\BACKEND"
python manage.py migrate
python poblar_datos.py
```

### 2. Verificar que los Servidores Estén Corriendo

- **Backend**: Ya está corriendo en el puerto 8000 ✓
- **Frontend**: Ya está corriendo en el puerto 5173 ✓

### 3. Probar el Sistema

#### Como Administrador:
1. Ve a http://localhost:5173/login
2. Ingresa:
   - Usuario: `admin`
   - Contraseña: `Admin123!`
3. Verás aparecer:
   - 🔔 **Notificaciones** de salones ocupados (si hay reservas hoy)
   - Menú: **Gestionar Salones** y **Gestionar Reservas**

**Funcionalidades Admin**:
- **Gestionar Salones**: 
  - Click en "Nuevo Salón" para crear
  - Click en "Editar" para modificar
  - Click en "Eliminar" para borrar
- **Gestionar Reservas**:
  - Ver todas las reservas
  - Aprobar/Rechazar pendientes
  - Eliminar cualquier reserva
  - Filtrar por estado

#### Como Docente:
1. Cierra sesión (logout)
2. Ingresa:
   - Usuario: `docente1`
   - Contraseña: `Docente123!`
3. Verás:
   - Menú: **Salones** y **Mis Reservas**
   - NO verás opciones de gestión (reservado para admin)

O prueba con el segundo docente:
   - Usuario: `docente2`
   - Contraseña: `Docente123!`

## 🎨 Características Implementadas

### ✅ Panel de Administración de Salones
- Tabla completa con todos los salones
- Crear salones con todos los detalles:
  - Nombre, código, tipo, bloque, piso
  - Capacidad, descripción
  - Equipamiento (proyector, aire, computadores, TV, audio, WiFi)
  - Estado (disponible, ocupado, mantenimiento)
- Editar cualquier salón
- Eliminar con confirmación

### ✅ Panel de Administración de Reservas
- Ver TODAS las reservas del sistema
- Filtrar por estado (todas, pendiente, aprobada, rechazada, cancelada, completada)
- Acciones rápidas:
  - ✓ Aprobar
  - ✗ Rechazar
  - 🗑 Eliminar
- Ver detalles: fecha, horario, salón, motivo, asistentes, usuario

### ✅ Sistema de Notificaciones
- Al iniciar sesión como admin, aparece notificación automática
- Muestra reservas aprobadas del día actual
- Info de cada reserva: motivo, horario, nombre del usuario
- Botón para ir directamente a gestionar reservas
- Se puede cerrar con ×

### ✅ Navegación Dinámica
- El menú cambia según el rol:
  - **Admin**: Salones | Gestionar Salones | Gestionar Reservas
  - **Docente**: Salones | Mis Reservas
- Protección de rutas: docentes no pueden acceder a /admin/*

## 📝 Usuarios Disponibles

| Usuario | Contraseña | Rol | Descripción |
|---------|-----------|-----|-------------|
| admin | Admin123! | Administrador | Acceso completo |
| docente1 | Docente123! | Docente | Carlos Martínez |
| docente2 | Docente123! | Docente | María González |

## 🚀 Próximos Pasos (Opcional)

Si quieres mejorar aún más el sistema:

1. **Seguridad**: Cambiar permisos del backend de `AllowAny` a `IsAuthenticated`
2. **UX**: Reemplazar `alert()` con notificaciones toast elegantes
3. **Reportes**: Exportar datos a Excel/PDF
4. **Estadísticas**: Dashboard con gráficos de ocupación
5. **Email**: Notificaciones por correo cuando se aprueba/rechaza una reserva

## ⚠️ Notas Importantes

- **NO CREAR MÁS TERMINALES**: Ya tienes 2 terminales corriendo (backend y frontend)
- Para aplicar la migración, usa una terminal temporal que cerrarás después
- Los cambios en el código del frontend se recargan automáticamente
- Los cambios en el backend Django se recargan automáticamente

## 🐛 Solución de Problemas

### Si las notificaciones no aparecen:
1. Verifica que existan reservas con estado "aprobada" y fecha de hoy
2. Crea una reserva de prueba y apruébala desde el panel admin

### Si no aparecen los menús de admin:
1. Verifica que ejecutaste `python poblar_datos.py`
2. Cierra sesión y vuelve a iniciar con `admin` / `Admin123!`
3. Refresca la página (F5)

### Si hay error 404 en rutas admin:
1. Verifica que el frontend está corriendo
2. Refresca la página
3. El router debería cargar las nuevas rutas automáticamente

## 📚 Archivos Importantes

Si necesitas revisar o modificar algo:

- **Admin Salones**: `FRONTEND/src/views/AdminSalones.vue`
- **Admin Reservas**: `FRONTEND/src/views/AdminReservas.vue`
- **Notificaciones**: `FRONTEND/src/components/AdminNotifications.vue`
- **Navegación**: `FRONTEND/src/components/Header.vue`
- **Rutas**: `FRONTEND/src/router/index.js`
- **API**: `FRONTEND/src/services/api.js`
- **Modelo Usuario**: `BACKEND/usuarios/models.py`

---

**¡Todo listo!** 🎉

El sistema ahora tiene roles completos de Admin y Docente con todas las funcionalidades solicitadas.
