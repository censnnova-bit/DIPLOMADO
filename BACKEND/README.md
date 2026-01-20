# GECOS Backend - Django REST API

Backend para el sistema GECOS (Gestión de Espacios) construido con Django 6.0.1 y Django REST Framework.

## 🚀 Características

- ✅ Django 6.0.1 (última versión)
- ✅ Django REST Framework 3.16.1
- ✅ CORS habilitado para desarrollo con Vue.js
- ✅ Configuración con variables de entorno (.env)
- ✅ SQLite como base de datos por defecto
- ✅ Configuración lista para desarrollo y producción
- ✅ Archivos estáticos y media configurados

## 📋 Requisitos Previos

- Python 3.13+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Activar el entorno virtual:**

```bash
# En Windows
.\venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

2. **Crear archivo .env:**

Copia el archivo `.env.example` a `.env` y personaliza las variables:

```bash
cp .env.example .env
```

3. **Aplicar migraciones:**

```bash
python manage.py migrate
```

4. **Crear superusuario:**

```bash
python manage.py createsuperuser
```

5. **Iniciar servidor de desarrollo:**

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📁 Estructura del Proyecto

```
BACKEND/
├── gecos_backend/          # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py         # Configuración de Django
│   ├── urls.py            # URLs principales
│   ├── asgi.py            # Configuración ASGI
│   └── wsgi.py            # Configuración WSGI
├── venv/                   # Entorno virtual de Python
├── manage.py              # Utilidad de línea de comandos
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Ejemplo de variables de entorno
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Este archivo
```

## 🔌 Endpoints Disponibles

- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **API Root:** `http://127.0.0.1:8000/api/`
- **API Auth:** `http://127.0.0.1:8000/api-auth/`

## 🛠️ Comandos Útiles

### Crear una nueva app Django:
```bash
python manage.py startapp nombre_app
```

### Crear migraciones:
```bash
python manage.py makemigrations
```

### Aplicar migraciones:
```bash
python manage.py migrate
```

### Ejecutar tests:
```bash
python manage.py test
```

### Recolectar archivos estáticos:
```bash
python manage.py collectstatic
```

## 🔐 Configuración de Seguridad

⚠️ **Importante para Producción:**

1. Cambia `SECRET_KEY` en el archivo `.env`
2. Establece `DEBUG=False`
3. Configura `ALLOWED_HOSTS` correctamente
4. Usa una base de datos robusta (PostgreSQL, MySQL)
5. Configura HTTPS
6. Revisa la configuración de CORS

## 📦 Paquetes Instalados

- **Django 6.0.1:** Framework web
- **djangorestframework 3.16.1:** API REST
- **django-cors-headers 4.9.0:** Manejo de CORS
- **python-decouple 3.8:** Gestión de variables de entorno
- **Pillow 12.1.0:** Procesamiento de imágenes

## 🌐 Conexión con Frontend

El backend está configurado para aceptar peticiones desde:
- `http://localhost:5173`
- `http://localhost:5174`

Modifica `CORS_ALLOWED_ORIGINS` en `settings.py` según tus necesidades.

## 📝 Notas Adicionales

- La configuración actual usa SQLite, ideal para desarrollo
- Para producción, considera usar PostgreSQL o MySQL
- Los archivos media se guardarán en la carpeta `media/`
- Los archivos estáticos se recolectarán en `staticfiles/`

## 🐛 Solución de Problemas

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: Database locked**
```bash
# Cierra todas las conexiones a la base de datos
# Reinicia el servidor
```

**Error: Port already in use**
```bash
# Usa un puerto diferente
python manage.py runserver 8001
```

## 📞 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.

---

Desarrollado con ❤️ para GECOS - Sistema de Gestión de Espacios
