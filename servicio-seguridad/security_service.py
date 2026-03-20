# servicio-seguridad/security_service.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import os
import shutil
from pathlib import Path

app = FastAPI(
    title="Servicio de Seguridad - Hash & Storage",
    description="Recibe imágenes, las hashea y las guarda de forma segura."
)

# Configuración CORS (ajustar según frontend)
#origins = ["http://localhost:3000", "http://127.0.0.1:3000","https://frontend-ui-vrgi.onrender.com"]
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# Agrega la URL exacta de tu frontend de Render (sin la barra final /)
# origins = [
#     "https://frontend-ui-vrgi.onrender.com"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins, 
#     allow_credentials=True,
#     allow_methods=["*"], # Permite GET, POST, OPTIONS, etc.
#     allow_headers=["*"], # Permite todos los headers (incluyendo Authorization)
# )

# Carpeta segura para almacenar imágenes
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

@app.get("/")
async def root():
    return {"status": "online", "service": "security-service"}

@app.post("/procesar-imagen")
async def procesar_imagen(file: UploadFile = File(...)):
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes.")

    # Leer bytes
    content = await file.read()

    # Calcular hash SHA-256
    file_hash = hashlib.sha256(content).hexdigest()
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    secure_filename = f"{file_hash}.{file_extension}"
    file_path = UPLOAD_DIR / secure_filename

    # Guardar archivo con nombre hasheado
    with open(file_path, "wb") as f:
        f.write(content)

    # Devolver ruta relativa segura
    secure_path = f"/uploads/{secure_filename}"
    
    return {
    "hash": file_hash,
    "ruta_imagen": str(UPLOAD_DIR / secure_filename), # Devolverá "/app/uploads/hash.jpg"
    "nombre_original": file.filename
    }