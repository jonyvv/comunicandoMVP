# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos (si tienes un requirements.txt)
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (el mismo que usas en uvicorn)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:gateway_app", "--host", "0.0.0.0", "--port", "8000"]