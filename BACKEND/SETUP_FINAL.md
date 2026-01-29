# 🚀 INSTRUCCIONES PARA COMPLETAR LA CONFIGURACIÓN

## Paso 1: Aplicar Migraciones

En la terminal de BACKEND, ejecuta:

```bash
cd BACKEND
source venv/Scripts/activate
python manage.py makemigrations
python manage.py migrate
```

## Paso 2: Poblar la Base de Datos

Ejecuta el comando personalizado que creará 10 salones y 3 usuarios:

```bash
python manage.py poblar_db
```

Este comando creará:

- ✅ 10 salones con diferentes características
- ✅ 3 usuarios de prueba con credenciales

## 🔑 CREDENCIALES DE PRUEBA

### 1. Administrador

- **Usuario:** `admin`
- **Contraseña:** `Admin123!`
- **Rol:** Administrador del sistema

### 2. Docente

- **Usuario:** `docente1`
- **Contraseña:** `Docente123!`
- **Rol:** Docente

## Paso 3: Iniciar el Servidor Backend

```bash
python manage.py runserver
```

El backend estará en: http://127.0.0.1:8000/

## 📡 ENDPOINTS DISPONIBLES

### Autenticación

- **POST** `/api/login/` - Iniciar sesión (devuelve token)
- **POST** `/api/logout/` - Cerrar sesión
- **GET** `/api/usuarios/me/` - Obtener usuario actual

### Salones

- **GET** `/api/salones/` - Listar todos los salones
- **GET** `/api/salones/{id}/` - Detalle de un salón
- **GET** `/api/salones/disponibles/` - Solo salones disponibles

### Reservas

- **GET** `/api/reservas/` - Listar reservas
- **POST** `/api/reservas/` - Crear nueva reserva
- **GET** `/api/reservas/mis_reservas/` - Reservas del usuario actual
- **POST** `/api/reservas/{id}/cancelar/` - Cancelar reserva
- **POST** `/api/reservas/{id}/confirmar/` - Confirmar reserva (solo admin)

## Paso 4: Ejemplo de Login desde Frontend

```javascript
// Login
const response = await fetch("http://127.0.0.1:8000/api/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    username: "admin",
    password: "Admin123!",
  }),
});

const data = await response.json();
// data.token contiene el token de autenticación
// data.user contiene la información del usuario

// Guardar token en localStorage
localStorage.setItem("token", data.token);

// Usar token en requests posteriores
const salonesResponse = await fetch("http://127.0.0.1:8000/api/salones/", {
  headers: {
    Authorization: `Token ${data.token}`,
  },
});
```

## 📝 NOTAS IMPORTANTES

1. El backend usa autenticación por **Token** (Django REST Framework)
2. Todos los endpoints requieren autenticación excepto `/api/login/`
3. Los tokens se guardan en la tabla `authtoken_token`
4. CORS está configurado para aceptar requests desde localhost:5173 y localhost:5174

## 🔧 Próximos Pasos - Frontend

Ahora necesitas:

1. Crear componente de Login en Vue
2. Implementar store de autenticación (Pinia o Vuex)
3. Proteger rutas que requieren autenticación
4. Conectar las vistas de salones con la API
5. Implementar formulario de reservas

¿Deseas que continúe con la implementación del frontend?
