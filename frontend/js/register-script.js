document.getElementById("registerBtn").addEventListener("click", async () => {

    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const responseText = document.getElementById("registerResponse");

    if (!email || !password) {
        responseText.innerText = "Completa todos los campos";
        responseText.style.color = "red";
        return;
    }

    try {
        const res = await fetch("https://api-gateway-9561.onrender.com/api/v1/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok) {
            responseText.innerText = "Usuario creado correctamente";
            responseText.style.color = "green";

            setTimeout(() => {
                window.location.href = "index.html";
            }, 1500);

        } else {
            responseText.innerText = data.error;
            responseText.style.color = "red";
        }

    } catch (err) {
        responseText.innerText = "Error de conexión";
        responseText.style.color = "red";
    }

});
