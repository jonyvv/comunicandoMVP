FROM python:3.12-slim

# Evitar interacciones y caché
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app


# Copiar requirements primero (mejor caché)
COPY ./requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Instalar google-generativeai si no está en requirements.txt
RUN pip install --no-cache-dir google-generativeai pillow

# Copiar todo el código del servicio
COPY ./api_ia/gemini-service.py /app/

# Crear carpeta para imágenes compartidas (opcional, docker-compose la montará)
RUN mkdir -p /uploads && chmod 777 /uploads

# Exponer puerto
EXPOSE 80

# Comando para ejecutar
CMD ["uvicorn", "gemini-service:app", "--host", "0.0.0.0", "--port", "80"]
