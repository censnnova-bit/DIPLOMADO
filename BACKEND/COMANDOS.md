# Comandos Rápidos - Django Backend

## Activar entorno virtual

```bash
# En Windows (PowerShell)
.\venv\Scripts\activate

# En Windows (Git Bash)
source venv/Scripts/activate

# En macOS/Linux
source venv/bin/activate
```

## Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Servidor disponible en: http://127.0.0.1:8000/

## Crear superusuario (admin)

```bash
python manage.py createsuperuser
```

## Crear nueva aplicación

```bash
python manage.py startapp nombre_app
```

Después de crear una app, agrégala a `INSTALLED_APPS` en `settings.py`

## Gestión de base de datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver SQL de migraciones
python manage.py sqlmigrate app_name 0001
```

## Comandos útiles

```bash
# Verificar proyecto
python manage.py check

# Shell interactivo
python manage.py shell

# Abrir consola de base de datos
python manage.py dbshell

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## Estructura recomendada para una app

```
mi_app/
├── __init__.py
├── admin.py           # Registro en el admin
├── apps.py            # Configuración de la app
├── models.py          # Modelos de base de datos
├── serializers.py     # Serializers de DRF (crear manualmente)
├── views.py           # Vistas y ViewSets
├── urls.py            # URLs de la app (crear manualmente)
├── tests.py           # Tests
└── migrations/        # Migraciones automáticas
```

## Instalación de paquetes adicionales

```bash
# Activar venv primero, luego:
pip install nombre_paquete

# Actualizar requirements.txt
pip freeze > requirements.txt
```
