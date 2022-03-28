import sys
from dataBase import BaseDatos
import pandas as pd
import datetime
import numpy as np
from SapServiceLayer import SapSL
import time


# Ruta del log y la variable del log
logPath = 'C:\\Users\\joro-ext\\Desktop\\log.txt'
log = '\n\nScript execution - ' + str(datetime.datetime.now())

# Ruta de los archivos
mainPath = 'C:\\Users\\joro-ext\\Desktop\\main.csv'
skuPath = 'C:\\Users\\joro-ext\\Desktop\\sku.csv'
prepacksPath = 'C:\\Users\\joro-ext\\Desktop\\prepacks.csv'

# Direccion de la Base de Datos
direccion = '10.52.104.154'
puerto = '30015'
usuario = 'SYSTEM'
clave = 'Innovate2018'

# Parametros ServiceLayer
URL = "https://10.52.104.154:50000/b1s/v1/"
dataBase = "ASTOR_MULLER_GERMANY_TESTDEV"
userName = "manager"
password = "Man#1234"


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
excelModels = pd.read_csv(mainPath, dtype=np.str)
excelSku = pd.read_csv(skuPath, dtype=np.str)
excelPrepacks = pd.read_csv(prepacksPath, dtype=np.str)
log += '\nFile read'

# Cabeceras del excel que no son UDFs
cabeceras = 'Code', 'Description', 'Segment code', 'Segment', 'Group code', 'Group', 'AF Segmentation', \
            'SAP Item Group', 'Season', 'Collection code', 'Collection', 'Producer', 'Designer shoe', 'Designer sole', \
            'Division code', 'Year', 'Country of Origin', 'Vendor', 'Main warehouse', 'Price List', 'Currency', \
            'Price', 'Size Chart', 'Color Code'


filaActual = excelModels.iloc[0]

print(filaActual)
