import sqlite3

def conectar():
    return sqlite3.connect("database.db")

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos

def insertar_producto(nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )
    conn.commit()
    conn.close()

def eliminar_producto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()

def obtener_producto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    dato = cursor.fetchone()
    conn.close()
    return dato

def actualizar_producto(id, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
        (nombre, precio, stock, id)
    )
    conn.commit()
    conn.close()