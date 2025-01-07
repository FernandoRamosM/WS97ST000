import sqlite3

def conn ():
    conexion = sqlite3.connect('static/db/stp97per0201.db')   # Crear o conectar a la base de datos
    return conexion