// ... CONFIGURACIÓN ...
const API_GATEWAY_URL = "https://api-gateway-9561.onrender.com/api/v1"; 

// Intentar obtener el token (solo existirá si ya nos logueamos)
let token = localStorage.getItem("token");

console.log("Sistema listo. Estado del token:", token ? "Cargado" : "No detectado");

// ========================== LÓGICA DE LOGIN ==========================
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
    console.log("Botón de Login detectado.");
    loginBtn.addEventListener("click", async () => {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const responseText = document.getElementById("response");

        try {
            const res = await fetch(`${API_GATEWAY_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                localStorage.setItem("token", data.token);
                console.log("Login exitoso, redirigiendo...");
                // Como index.html y traductor.html están en la misma carpeta, 
                // la ruta es directa:
                window.location.href = "../htmlycss/traductor.html";
            } else {
                responseText.innerText = data.error || "Credenciales incorrectas";
                responseText.style.color = "red";
            }
        } catch (err) {
            console.error("Error al conectar con el Gateway:", err);
        }
    });
}

// ========================== LÓGICA DE TRADUCTOR ==========================
const btnTranslate = document.getElementById('btnTranslate');
const previewImage = document.getElementById('previewImage');
if (imageInput && previewImage) {
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            // Creamos una URL temporal que solo el navegador entiende
            const urlTemporal = URL.createObjectURL(file);
            previewImage.src = urlTemporal;
            previewImage.style.display = 'block';
            console.log("Vista previa cargada correctamente");
        }
    });
}
if (btnTranslate) {
    console.log("Botón de Traductor detectado.");
    btnTranslate.addEventListener('click', async () => {
        const imageFile = document.getElementById('imageInput').files[0];
        const output = document.getElementById('output');

        if (!imageFile) {
            output.innerHTML = "<strong>⚠️ Error:</strong> Selecciona una imagen.";
            return;
        }

        const formData = new FormData();
        formData.append('file', imageFile); 
        output.innerHTML = "Traduciendo con IA...";

        try {
            // Refrescamos el token antes de enviarlo por si acaso
            token = localStorage.getItem("token");

            const response = await fetch(`${API_GATEWAY_URL}/traduccion`, {
                method: 'POST',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {},
                body: formData 
            });

            const data = await response.json();

            if (!response.ok) {
                output.innerHTML = `<h2>❌ Error:</h2> <p>${data.detail || "Error en el proceso."}</p>`;
                return;
            }

            const translatedText = data.traduccion || data.resultado_traduccion || "No se pudo interpretar.";
            output.innerHTML = `<h2>✅ Traducción Exitosa</h2><p><strong>Resultado LSA:</strong> ${translatedText}</p>`;
            
        } catch (error) {
            output.innerHTML = `<h2>⚠️ Error de conexión</h2><p>Verifica el API Gateway.</p>`;
        }
    });
}