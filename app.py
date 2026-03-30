from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "clave123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def conectar():
    return sqlite3.connect("database.db")

class Usuario(UserMixin):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

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

def crear_tablas():
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        stock INTEGER
    )
    """)

    conn.commit()
    conn.close()

crear_tablas()

@app.route('/')
def inicio():
    return redirect('/login')

@app.route('/registro', methods=['GET','POST'])
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

@app.route('/login', methods=['GET','POST'])
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

@app.route('/dashboard')
@login_required
def dashboard():
    return "Bienvenido " + current_user.nombre

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# CRUD

@app.route('/productos')
@login_required
def productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return render_template('productos/listar.html', productos=datos)

@app.route('/productos/nuevo', methods=['GET','POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                       (nombre, precio, stock))
        conn.commit()
        conn.close()

        return redirect('/productos')

    return render_template('productos/form.html')

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

@app.route('/productos/editar/<int:id>', methods=['GET','POST'])
@login_required
def editar(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        cursor.execute("UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
                       (nombre, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect('/productos')

    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = cursor.fetchone()
    conn.close()

    return render_template('productos/form.html', producto=producto)

@app.route('/reporte')
@login_required
def reporte():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for p in productos:
        pdf.cell(200,10, txt=f"{p[1]} - {p[2]} - {p[3]}", ln=True)

    pdf.output("reporte.pdf")

    return "Reporte generado"

if __name__ == '__main__':
    app.run(debug=True)
    