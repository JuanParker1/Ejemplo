import sys
from dataBase import BaseDatos
import pandas as pd
import datetime
import numpy as np
from SapServiceLayer import SapSL

# Ruta del Excel
excelPath = 'C:\\Users\\Test4\\Desktop\\prepacks.csv'

# Direccion de la Base de Datos
direccion = '192.168.0.22'
puerto = '30015'
usuario = 'SYSTEM'
clave = 'Argns1050'

# Parametros ServiceLayer
URL = "https://192.168.0.22:50000/b1s/v1/"
dataBase = "SBODEMOAR3"
userName = "manager"
password = "1234"

# Variables
todoBien = True
fechaHoraEjecucion = datetime.datetime.now()

# Ruta del log y la variable del log
logPath = 'C:\\Users\\Test4\\Desktop\\log.txt'
log = '\n\nScript execution - ' + str(fechaHoraEjecucion)

# Generamos la conexion con la base de datos
db = BaseDatos(direccion, puerto, usuario, clave)

# Conexion al Service Layer
conexionServicio = SapSL(URL, dataBase, userName, password)
if not conexionServicio.connectedStatus():
    log += '\nFatal error: No connection with Sap ServiceLayer...'
    f = open(logPath, "a")
    f.write(log)
    f.close()
    print(log)
    exit()
log += '\nConnected to Sap Service Layer'

# Leemos los campos desde el excel
log += '\nReading file ' + excelPath
excelPrepacks = pd.read_csv(excelPath, dtype=np.str)
log += '\nFile read'

for nlinea in range(len(excelPrepacks)):
    filaActual = excelPrepacks.iloc[nlinea]

    # [6300, 8000, 4700, ... ]
    #coloresModelo = db.consultarFilas(
    #    'SELECT "U_ColCode" FROM "' + dataBase + '"."@ARGNS_MODEL_COLOR" WHERE "Code" = ' + "'" + + "'")
    # {ntalle: cantidad, ntalle: cantidad, ... }
    # tallesEscala =




