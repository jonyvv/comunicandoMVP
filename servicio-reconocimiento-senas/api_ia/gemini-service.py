from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from PIL import Image
import os
import google.generativeai as genai
import io
# Obtener la clave API desde la variable de entorno
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise HTTPException(status_code=500, detail="La clave API de Gemini no está configurada.")

# Configurar la API con la clave
genai.configure(api_key=api_key)

app = FastAPI()

UPLOAD_DIR = "/app/uploads"

#@app.post("/reconocer-sena-por-ruta")
# async def reconocer_sena_por_ruta(file: UploadFile = File(...), 
#     nombre_seguro: str = Form(...)):
#     ruta_relativa = data.get("ruta_imagen")

#     if not os.path.exists(ruta_relativa):
#             # Intento B: Si seguridad mandó solo el nombre, lo unimos
#             nombre_archivo = os.path.basename(ruta_relativa)
#             ruta_final = os.path.join(UPLOAD_DIR, nombre_archivo)
#     else:
#         ruta_final = ruta_relativa
#     if not os.path.exists(ruta_final):
#         raise HTTPException(status_code=404, detail=f"No se encontró: {ruta_final}")
    
#     nombre_archivo = os.path.basename(ruta_relativa)
#     ruta_absoluta = os.path.join(UPLOAD_DIR, nombre_archivo)
    
#     if not os.path.exists(ruta_absoluta):
#         raise HTTPException(status_code=404, detail="La imagen no existe en el volumen compartido")


#     try:
#         img = Image.open(ruta_absoluta)
#         prompt = "Traduce esa seña de las manos (lenguaje de señas argentino a español). Solo la palabra o frase, sin explicaciones."
#         # Cambiar el modelo a uno compatible y disponible en 2025
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         response = model.generate_content([img, prompt])

#         return {
#             "seña_detectada": "Gesto de mano",
#             "resultado_traduccion": response.text.strip(),
#             "modelo_usado": "gemini-2.5-flash",
#             "ruta_usada": ruta_relativa
#         }
#     except Exception as e:
#         print(f"Error en IA: {str(e)}")  # Depuración opcional
#         raise HTTPException(status_code=500, detail=f"Error en IA: {str(e)}")


@app.post("/reconocer-sena")
async def reconocer_sena(file: UploadFile = File(...), nombre_seguro: str = Form(...)):
    # 1. Leemos los bytes del archivo
    content = await file.read()
    
    # Log para confirmar que los bytes llegaron al servicio
    print(f"DEBUG IA: Procesando imagen: {nombre_seguro}")
    print(f"DEBUG IA: Tamaño del archivo recibido: {len(content)} bytes")

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="El archivo recibido está vacío")

    try:
<<<<<<< HEAD
        img = Image.open(ruta_absoluta)
        prompt = "Traduce esa seña de las manos (lenguaje de señas argentino a español). Solo la palabra o frase, sin explicaciones y en español"
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([img, prompt])
=======
        # 2. Creamos el stream de bytes y REBOBINAMOS al inicio
        img_stream = io.BytesIO(content)
        img_stream.seek(0)  # <--- ESTO SOLUCIONA EL 'cannot identify image file'
>>>>>>> 11d1ff3d9850d4123bc1c1569c97574a52eba506

        # 3. Abrimos la imagen con Pillow
        img = Image.open(img_stream)
        
        # 4. Configuramos y llamamos a Gemini
        # Importante: Usa gemini-1.5-flash (el 2.5 no existe)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = (
            "traduce la seña de LSA a texto"
            "Responde solo con la palabra o frase traducida."
        )
        
        response = model.generate_content([img, prompt])
        
        # 5. Retornamos el resultado
        traduccion = response.text.strip() if response.text else "No se pudo interpretar"
        
        return {
            "seña_detectada": "Gesto procesado",
            "resultado_traduccion": traduccion,
            "status": "success"
        }

    except Exception as e:
        print(f"ERROR CRÍTICO EN IA: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar imagen: {str(e)}")

@app.get("/")
async def root():
    return {"status": "online", "service": "AI-service"}