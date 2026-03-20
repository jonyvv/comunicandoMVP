document.getElementById("loginBtn").addEventListener("click", async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const responseText = document.getElementById("response");

    const res = await fetch("https://api-gateway-9561.onrender.com/api/v1/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
        // Guardar token
        localStorage.setItem("token", data.token);

        // Redirigir al frontend principal
        window.location.href = "/htmlycss/traductor.html";
    } else {
        responseText.innerText = data.error;
        responseText.style.color = "red";
    }
});
