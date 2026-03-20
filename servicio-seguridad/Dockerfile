FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./security_service.py /app/

# Crear carpeta uploads dentro de /app
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

EXPOSE 80

CMD ["uvicorn", "security_service:app", "--host", "0.0.0.0", "--port", "80"]