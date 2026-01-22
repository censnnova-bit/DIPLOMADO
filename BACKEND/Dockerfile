# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes de Python si fuera necesario
# (aunque para este proyecto simple puede no ser necesario, es buena práctica)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para correr el servidor (usando runserver para mantenerlo simple y compatible con desarrollo)
# En un entorno real de producción se recomendaría usar Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
