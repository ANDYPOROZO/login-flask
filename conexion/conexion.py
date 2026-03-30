import pymysql

def conectar():
    return pymysql.connect(
        host="127.0.0.1",
        user="flaskuser",
        password="12345",
        database="tienda"
    )