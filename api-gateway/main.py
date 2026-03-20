from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import io

# URLs de los microservicios
SERVICE_SEGURIDAD_URL = "https://servicio-seguridad.onrender.com/procesar-imagen"
SERVICE_IA_URL = "https://servicio-reconocimiento-senas.onrender.com/reconocer-sena"
SERVICE_LOGIN_URL = "https://backend-login-qfqo.onrender.com/login"
SERVICE_REGISTER_URL = "https://backend-login-qfqo.onrender.com/register"
gateway_app = FastAPI(title="API Gateway - Comunicando")

origins = ["*"]
gateway_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@gateway_app.get("/")
async def health_check():
    return {"status": "API Gateway is running"}

#@gateway_app.post("/api/v1/traduccion")
# async def route_traduccion_sena(file: UploadFile = File(...)):
#     # 1. Leemos el contenido una sola vez
#     content = await file.read()
    
#     async with httpx.AsyncClient() as client:
#         # 2. Enviar a Seguridad para hashear y guardar
#         files = {'file': (file.filename, content, file.content_type)}
#         try:
#             seg_res = await client.post(SERVICE_SEGURIDAD_URL, files=files, timeout=20.0)
#             if seg_res.status_code != 200:
#                 raise HTTPException(status_code=500, detail="Error en Servicio de Seguridad")
            
#             ruta_segura = seg_res.json()["ruta_imagen"]

#             # 3. Enviar la ruta obtenida al servicio de IA
#             ia_res = await client.post(
#                 SERVICE_IA_URL, 
#                 json={"ruta_imagen": ruta_segura}, 
#                 timeout=60.0
#             )
            
#             if ia_res.status_code == 200:
#                 return ia_res.json()
#             else:
#                 raise HTTPException(status_code=ia_res.status_code, detail="Error en Servicio de IA")
                
#         except httpx.ConnectError:
#             raise HTTPException(status_code=503, detail="Servicios internos no alcanzables")   

@gateway_app.post("/api/v1/traduccion")
async def route_traduccion_sena(file: UploadFile = File(...)):
    # 1. Leer contenido una vez
    content = await file.read()
    filename = file.filename
    content_type = file.content_type

    async with httpx.AsyncClient() as client:
        # 2. SEGUIRIDAD: Enviamos para hashear y guardar
        files_seg = {'file': (filename, content, content_type)}
        seg_res = await client.post(SERVICE_SEGURIDAD_URL, files=files_seg, timeout=20.0)
        
        if seg_res.status_code != 200:
            raise HTTPException(status_code=500, detail="Error en Seguridad")
        
        # Extraemos el hash/nombre que generó Seguridad
        datos_seguridad = seg_res.json()
        hash_generado = datos_seguridad.get("hash") 
        nombre_con_extension = os.path.basename(datos_seguridad.get("ruta_imagen"))

        # 3. IA: Enviamos los bytes + el nombre hasheado
        # Usamos 'data' para el Form y 'files' para los bytes
        payload_ia = {'nombre_seguro': nombre_con_extension}
        files_ia = {'file': (nombre_con_extension, content, content_type)}
        
        ia_res = await client.post(
            "https://servicio-reconocimiento-senas.onrender.com/reconocer-sena",
            data=payload_ia,
            files=files_ia,
            timeout=60.0
        )
        
        if ia_res.status_code == 200:
            return ia_res.json()
        else:
            raise HTTPException(status_code=ia_res.status_code, detail="Error en IA")

# Endpoint para login
@gateway_app.post("/api/v1/login")
async def login_proxy(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            # Enviamos el payload al servicio 'backend' en el puerto 5000
            response = await client.post(SERVICE_LOGIN_URL, json=payload, timeout=10.0)
            
            # Esto propaga el error (401, 404, etc.) si el backend falla
            if response.status_code != 200:
                # Intentamos extraer el error del backend, si no, uno genérico
                detail = response.json().get("error", "Error en autenticación")
                raise HTTPException(status_code=response.status_code, detail=detail)
                
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Servicio de Autenticación no disponible")
        
# Endpoint para register
@gateway_app.post("/api/v1/register")
async def register_proxy(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERVICE_REGISTER_URL,
                json=payload,
                timeout=10.0
            )

            if response.status_code != 201:
                detail = response.json().get("error", "Error en registro")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=detail
                )

            return response.json()

        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Servicio de Registro no disponible"
            )
