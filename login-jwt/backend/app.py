from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret")

def init_db():
    db_path = "db/app.db"
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if not cursor.fetchone():
        try:
            # Buscamos el archivo subiendo un nivel desde 'backend' hacia 'init'
            base_path = os.path.abspath(os.path.dirname(__file__)) # carpeta 'backend'
            sql_file_path = os.path.join(base_path, "..", "init", "init.sql")
            
            print(f"Buscando SQL en: {sql_file_path}")
            
            with open(sql_file_path, "r") as f:
                sql_script = f.read()
            
            conn.executescript(sql_script)
            conn.commit()
            print("Tablas creadas y usuario admin insertado con éxito.")
        except Exception as e:
            print(f"Error al ejecutar init.sql: {e}")
    else:
        print("La base de datos ya está inicializada.")
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect("db/app.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, email, password_hash FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password requeridos"}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()

    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 409

    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, password_hash)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

@app.route("/")
def index():
    return jsonify({"message": "Backend funcionando correctamente"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
