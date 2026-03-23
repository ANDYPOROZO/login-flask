import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="tienda"
    )
    print("CONEXIÓN EXITOSA")
except Exception as e:
    print("ERROR:", e)