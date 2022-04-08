import sqlite3

from debugpy import connect

conexion = sqlite3.connect("ejemplo.db")

# Creamos un cursor
cursor = conexion.cursor()
cursor.execute("CREATE TABLE estudiantes (email VARCHAR (100), carrera VARCHAR (100), nombre VARCHAR(100), edad INTEGER)")

conexion.close()