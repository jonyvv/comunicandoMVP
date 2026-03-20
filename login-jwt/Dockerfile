# Imagen base liviana con Python
FROM python:3.12-slim

# Evita que Python genere .pyc y fuerza logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements desde la subcarpeta backend
COPY backend/requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# --- CAMBIO CRUCIAL AQUÍ ---
# Copiamos AMBAS carpetas para que la ruta relativa funcione
COPY backend/ ./backend
COPY init/ ./init

# Creamos la carpeta donde vive la DB y damos permisos de escritura
# Importante: La ruta debe coincidir con lo que pusiste en app.py
RUN mkdir -p backend/db && chmod 777 backend/db

# Exponemos el puerto de Flask
EXPOSE 5000

# Comando de arranque (ejecutamos desde /app)
CMD ["python", "backend/app.py"]