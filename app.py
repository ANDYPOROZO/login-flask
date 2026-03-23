from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = "clave123"

# 🔐 LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# 🔌 CONEXIÓN SQLITE
def conectar():
    return sqlite3.connect("database.db")

# 👤 MODELO USUARIO
class Usuario(UserMixin):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

# 🔄 CARGAR USUARIO
@login_manager.user_loader
def load_user(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return Usuario(user[0], user[1])
    return None

# 🧱 CREAR TABLA
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

crear_tabla()

# 🧑 REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                       (nombre, email, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('registro.html')

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND password=?",
                       (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            usuario = Usuario(user[0], user[1])
            login_user(usuario)
            return redirect('/dashboard')

    return render_template('login.html')

# 🚪 LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# 🔒 DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    return "Bienvenido " + current_user.nombre

# 🏠 INICIO
@app.route('/')
def inicio():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)