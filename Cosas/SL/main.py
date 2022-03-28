import sys
from dataBase import BaseDatos
import pandas as pd
import datetime
import numpy as np
from SapServiceLayer import SapSL

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                  --- DEFINICIONES ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Variables
todoBien = True
fechaHoraEjecucion = datetime.datetime.now()

# Ruta del Excel
excelPath = 'C:\\Users\\Test4\\Desktop\\examples_.xlsx'

# Ruta del log y la variable del log
logPath = 'C:\\Users\\Test4\\Desktop\\log.txt'
simpleLogPath = 'C:\\Users\\Test4\\Desktop\\simpleLog.txt'
log = '\n\nScript execution - ' + str(fechaHoraEjecucion)
simpleLog = '\n\nScript execution - ' + str(fechaHoraEjecucion)

# Direccion de la Base de Datos
direccion = '192.168.0.22'
puerto = '30015'
usuario = 'SYSTEM'
clave = 'Argns1050'

# Parametros ServiceLayer
URL = "https://192.168.0.22:50000/b1s/v1/Login"
dataBase = "SBODEMOAR"
userName = "manager"
password = "1234"
conexionServicio = SapSL(URL, dataBase, userName, password)
if not conexionServicio.connectedStatus():
    log += '\nFatal error: No connection with Sap ServiceLayer...'
    simpleLog += '\nFatal error: No connection with Sap ServiceLayer...'
    f = open(logPath, "a")
    f.write(log)
    f.close()
    fs = open(simpleLogPath, "a")
    fs.write(simpleLog)
    fs.close()
    print('\nFatal error: No connection with Sap ServiceLayer...')
    exit()
print('Connected to Sap Service Layer')


# Atributos que hay que ir a checkear si existen, y en caso de que no lo hagan, crearlos (No Obligatorios = NO)
fkValuesNO = {'Segment code': '@ARGNS_PRODLINE', 'Group code': '@ARGNS_MODELGRP',
              'Season': '@ARGNS_SEASON', 'Collection code': '@ARGNS_COLLECTION', 'Year': '@ARGNS_YEAR',
              'Producer': '@ARGNS_BRAND', 'Division code': '@ARGNS_DIV'}

# Atributos que hay que ir a checkear si existen, y en caso de que no lo hagan, tirar un error en el log (Obligatorios)
fkValuesO = {'SAP Item Group': 'OITB', 'Designer shoe': 'OHEM', 'Designer sole': 'OUSR',
             'Main warehouse': 'OWHS', 'Price List': 'OPLN', 'Currency': 'OCRN'}

# Lo mismo de la linea de arriba, solo que ahora se pone el nombre de la PK
fkKeysO = {'SAP Item Group': 'ItmsGrpCod', 'Designer shoe': 'empID', 'Designer sole': 'USERID',
           'Main warehouse': 'WhsCode', 'Price List': 'ListName', 'Currency': 'CurrCode'}

# Cabeceras del excel
cabeceras = 'Code', 'Description', 'Segment code', 'Segment', 'Group code', 'Group', 'AF Segmentation', \
            'SAP Item Group', 'Season', 'Collection code', 'Collection', 'Producer', 'Designer shoe', 'Designer sole', \
            'Division code', 'Year', 'Country of Origin', 'Vendor', 'Main warehouse', 'Price List', 'Currency', \
            'Price', 'Size Chart', 'Color Code'

# Tipos de datos (para no eliminar los ceros iniciales, por ejemplo, para que 0001 no quede 1, sino 0001)
types = {'Segment code': np.str, 'Group code': np.str, 'AF Segmentation': np.str,
         'Season': np.str, 'Collection code': np.str, 'Year': np.str,
         'Producer': np.str, 'Division code': np.str, 'Size Chart': np.str,
         'Color Code': np.str, 'SAP Item Group': np.str, 'Designer shoe': np.str, 'Designer sole': np.str,
         'Vendor': np.str,
         'Main warehouse': np.str, 'Price List': np.str, 'Currency': np.str}

# Generamos la conexion con la base de datos
db = BaseDatos(direccion, puerto, usuario, clave)

# Leemos los campos desde el excel
excelModels = pd.read_excel(excelPath, sheet_name='ex_main', dtype=types)
excelSku = pd.read_excel(excelPath, sheet_name='ex_sku', dtype=types)
excelPrepacks = pd.read_excel(excelPath, sheet_name='ex_prepacks', dtype=types)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES MODELOS ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# - Definicion de Funciones -
def relacionarVendors(db, model, vendors):
    # El nombre del model, el codigo visible para el usuario
    ultimo = int(db.consultar('SELECT MAX(CAST("Code" AS int)) FROM "SBODEMOAR"."@ARGNS_MODVENDOR"')) + 1
    count = 0
    if len(vendors) > 1:
        for b in range(1, len(vendors)):
            consultaCheckeo = 'SELECT 1 FROM "SBODEMOAR"."@ARGNS_MODVENDOR" WHERE "U_ModCode" = '
            consultaCheckeo += "'" + model + "' AND "
            consultaCheckeo += '"U_CardCode" = '
            consultaCheckeo += "'" + vendors[b] + "'"
            checkeo = db.consultar(consultaCheckeo)
            if checkeo == '':
                vendorName = db.consultar(
                    'SELECT "CardName" FROM "SBODEMOAR"."OCRD" WHERE "CardCode" =' + "'" + vendors[b] + "'")
                if count == 0:
                    sentencia = 'INSERT INTO "SBODEMOAR"."@ARGNS_MODVENDOR" ("Code","Name","U_ModCode","U_CardCode",' \
                                '"U_CardName","U_CardType","U_DefBP") VALUES (' + "'" \
                                + str(ultimo) + "', '" + str(ultimo) + "', '" + model + "', '" + "" \
                                                                                                 "" + vendors[
                                    b] + "', '" + vendorName + "', 'S', 'Y')"
                else:
                    sentencia = 'INSERT INTO "SBODEMOAR"."@ARGNS_MODVENDOR" ("Code","Name","U_ModCode","U_CardCode",' \
                                '"U_CardName","U_CardType","U_DefBP") VALUES (' + "'" \
                                + str(ultimo) + "', '" + str(ultimo) + "', '" + model + "', '" + "" \
                                                                                                 "" + vendors[
                                    b] + "', '" + vendorName + "', 'S', 'N')"
                db.ejecutar(sentencia)
            ultimo += 1
            count += 1


def asociarColores(db, model, colors):
    # model = el codigo que aparece como PK en la tabla
    c = 1
    for color in colors:
        asegurarExistenciaColor(db, color)
        db.ejecutar(
            'INSERT INTO "SBODEMOAR"."@ARGNS_MODEL_COLOR" ("Code", "LineId", "Object", "U_ColCode", "U_Active")' + " VALUES ("
                                                                                                                   "'" + model + "', '" + str(
                c) + "', 'ARGNS_MODEL', '" + color + "', 'Y')")
        c += 1


def asegurarExistenciaColor(db, color):
    # Ingresa color como parametro y lo busca, si no existe, lo crea; Si existe, no hace nada
    a = db.consultar('SELECT 1 FROM "SBODEMOAR"."@ARGNS_COLOR" WHERE "U_ColCode"=' + "'" + color + "'")
    if a == '':
        ultimo = int(db.consultar('SELECT MAX("DocEntry") FROM "SBODEMOAR"."@ARGNS_COLOR"')) + 1
        db.ejecutar(
            'INSERT INTO "SBODEMOAR"."@ARGNS_COLOR" ("Code","DocEntry","Canceled","Object","U_ColCode","U_ColDesc","U_Active","U_RefColor") VALUES' + " ("
                                                                                                                                                      "'" + str(
                ultimo) + "', '" + str(ultimo) + "', 'N', 'ARGNS_COLOR', '" + color + "', '" + color + "', 'Y', 'N')")
        ultimo += 1


def segmentaciones(db, segmentacion):
    # 'AF Segmentation': '@ARGNS_APPTEXGRPS',
    # Primero ir a checkear si existe, si lo hace, retornar su codigo
    a = db.consultar('SELECT "Code" FROM "SBODEMOAR"."@ARGNS_APPTEXGRPS" WHERE "Name"=' + "'" + segmentacion + "'")
    if a != '':
        return a

    # Suponiendo que no existia, crearlo y retornar el codigo
    ult = int(db.consultar('SELECT MAX(CAST("DocEntry" AS int)) FROM "SBODEMOAR"."@ARGNS_APPTEXGRPS"')) + 1
    ejecucion = 'INSERT INTO "SBODEMOAR"."@ARGNS_APPTEXGRPS" ' \
                '("Code","Name","DocEntry","Canceled","Object","U_UseMod","U_UseCol","U_UseScl",' \
                '"U_ModLen","U_ColLen","U_SizeLen","U_Active", "U_Model", "U_Color", "U_Scale", "U_Sep") VALUES' + "" \
                                                                                                                   "('" + str(
        ult) + "', '" + segmentacion + "', '" + str(ult) + "', 'N', 'ARGNS_APPTEXGRPS', 'Y', 'Y','Y', " \
                                                           "'23', '6', '6', 'Y', 'Modelo', 'Color', 'Talla', '-')"
    db.ejecutar(ejecucion)
    return str(ult)


def escala(db, escala, model):
    # Primero ir a checkear si existe, si lo hace, retornar su codigo, si no existe, excepcion
    a = db.consultar('SELECT "Code" FROM "SBODEMOAR"."@ARGNS_SCALE" WHERE "U_SclCode"=' + "'" + escala + "'")
    if a != '':
        asociarEscalas(db, a.replace(' ', ''), escala, model)
        return a
    raise Exception('Scale not found...')


def asociarEscalas(db, escala, escalaNombre, model):
    # Se supone que la escala ya existe
    # Primero traemos todos los numeros de la escala de la tabla "SBODEMOAR"."@ARGNS_SIZE"
    lst = db.consultarArreglo('SELECT "U_SizeCode" FROM "SBODEMOAR"."@ARGNS_SIZE" WHERE "Code" =' + "'" + escala + "'")
    numeros = []
    for a in lst:
        if a != ' ':
            numeros.append(a)

    # Despues los asociamos con el model en la tabla "SBODEMOAR"."@ARGNS_MODEL_SIZE"
    c = 1
    for a in numeros:
        line = str(c)
        query = 'INSERT INTO "SBODEMOAR"."@ARGNS_MODEL_SIZE" ' \
                '("Code", "LineId", "Object", "U_SizeCod", "U_Selected", "U_SclCode", "U_VOrder") VALUES ('
        query += "'" + model + "', '" + line + "', 'ARGNS_MODEL', '" + a + "', 'Y', '" + escalaNombre + "', '" + line
        query += "')"
        db.ejecutar(query)
        c += 1


print('Starting...')
# - Modelos -
# Vamos recorriendo las filas
line = 0
for a in range(len(excelModels)):
    errores = False
    line += 1
    log += '\n\nEXCEL LINE ' + str(line) + ' - MODELS\n'
    try:
        todoBien = True

        # Cargamos los datos de la fila leida
        diccionarioTemporal = {}
        for b in cabeceras:
            diccionarioTemporal[b] = str(excelModels[b][a])

        # Checkeamos que el modelo no exista, y si lo hace seguimos con el siguiente modelo
        respuesta = db.consultar('SELECT 1 FROM "SBODEMOAR"."@ARGNS_MODEL" WHERE "U_ModCode"=' + "'" + str(diccionarioTemporal['Code']) + "'")
        if '1' in respuesta:
            print('Model ' + diccionarioTemporal['Code'] + ' already exists. Skipped')
            log += '\nModel ' + diccionarioTemporal['Code'] + ' already exists. Skipped'
            simpleLog += '\nModel ' + diccionarioTemporal['Code'] + ' already exists. Skipped'
            db.revert()
            continue

        # Traida de datos
        pkPriceList = db.consultar(
            'SELECT "ListNum" FROM "SBODEMOAR"."OPLN"T0 WHERE T0."ListName"=' + "'" + diccionarioTemporal[
                'Price List'] + "'")

        # Checkeamos que no hayan nulls
        if str(diccionarioTemporal['Price']) == 'nan' or str(diccionarioTemporal['Price']) == 'nan':
            diccionarioTemporal['Price'] = '0'

        # Nos aseguramos de que todos los campos que tengan que existir, lo hagan (dejar un error en caso contrario)
        for b in fkValuesO:
            buscar = diccionarioTemporal[b]
            if 'Designer shoe' == b and str(buscar) == 'nan':
                diccionarioTemporal[b] = ''
            elif 'Designer sole' == b and str(buscar) == 'nan':
                diccionarioTemporal[b] = ''
            else:
                c = db.consultar(
                    'SELECT 1 FROM "SBODEMOAR"."' + fkValuesO[b] + '"' + ' WHERE "' + fkKeysO[b] + '"' + "='" + str(
                        buscar) + "'")
                if '1' not in c:
                    todoBien = False
                    log += '\n"' + str(buscar) + '" not found in table "' + fkValuesO[b] + '" (column "' + fkKeysO[b] + '")'
                    print(str(buscar) + '" not found in table "' + fkValuesO[b] + '" (column "' + fkKeysO[b] + '")')
        if not todoBien:
            log += '\n1 or more critical values not found. Stopping...'
            raise Exception('1 or more critical values not found. Stopping...')
        else:
            log += '\nAll critical values found... Checking Vendors'

        todoBien = True
        # Nos aseguramos de que todos los vendor a relacionar, existan
        vendedores = diccionarioTemporal['Vendor'].replace(' ', '').split(';')
        for b in vendedores:
            c = db.consultar('SELECT 1 FROM "SBODEMOAR"."OCRD" WHERE "CardCode"' + "='" + b + "'")
            if '1' not in c:
                todoBien = False
                log += '\nVendor "' + b + '" not found in table "OCRD"'
        if not todoBien:
            log += '\n1 or more vendors not found. Stopping...'
            raise Exception('1 or more vendors not found. Stopping...')
        else:
            log += '\nAll critical values found... Checking Vendors'

        relacionarVendors(db, diccionarioTemporal['Code'], vendedores)

        # Nos aseguramos de que todos los campos que tengan que existir, lo hagan (crearlos en caso contrario)
        maximo1 = str(int(db.consultar('select MAX("DocEntry") from "SBODEMOAR"."@ARGNS_MODEL"T0')) + 1)
        maximo2 = str(int(db.consultar('select MAX("Code") from "SBODEMOAR"."@ARGNS_MODEL"T0')) + 1)
        if maximo1 > maximo2:
            maximo = maximo1
        else:
            maximo = maximo2
        colores = diccionarioTemporal['Color Code'].replace(' ', '').split(';')
        numero_modelo = maximo
        asociarColores(db, numero_modelo, colores)
        codigo_segmentacion = segmentaciones(db, diccionarioTemporal['AF Segmentation'])
        escala(db, diccionarioTemporal['Size Chart'], numero_modelo)
        for b in fkValuesNO:
            buscar = diccionarioTemporal[b]
            c = db.consultar(
                'SELECT 1 FROM "SBODEMOAR"."' + fkValuesNO[b] + '" WHERE "Code"' + "='" + str(buscar) + "'")
            if '1' not in c:
                log += '\n' + str(buscar) + ' not found in table ' + fkValuesNO[b] + ' (column "Code"). Creating...'
                if 'Segment code' == b:
                    consulta = db.consultar('select MAX("DocEntry") from "SBODEMOAR"."' + fkValuesNO[b] + '"T0')
                    if consulta is False or 'None' in consulta or consulta == '':
                        maximoSegment = str(0)
                    else:
                        maximoSegment = str(int(consulta) + 1)
                    if not db.ejecutar(
                            'INSERT INTO "SBODEMOAR"."' + fkValuesNO[
                                b] + '" ("DocEntry","Code","Name","Canceled","Object","U_Active") VALUES ' +
                            "('" + maximoSegment + "', '" + str(buscar) + "', '" + diccionarioTemporal[
                                'Segment'] + "', 'N', 'ARGNS_PRODLINE', 'Y')"):
                        errores = True
                elif 'Group code' == b:
                    if not db.ejecutar('INSERT INTO "SBODEMOAR"."' + fkValuesNO[b] + '" ("Code","Name","U_Active") VALUES ' +
                                "('" + str(buscar) + "', '" + diccionarioTemporal['Group'] + "', 'Y')"):
                        errores = True
                elif 'Season' == b:
                    if not db.ejecutar('INSERT INTO "SBODEMOAR"."' + fkValuesNO[b] + '" ("Code","Name","U_Active") VALUES ' +
                                "('" + str(buscar) + "', '" + str(buscar) + "', 'Y')"):
                        errores = True
                elif 'Collection code' == b:
                    consulta = db.consultar('select MAX("DocEntry") from "SBODEMOAR"."' + fkValuesNO[b] + '"T0')
                    if consulta is False or 'None' in consulta or consulta == '':
                        maximoCollection = str(0)
                    else:
                        maximoCollection = str(int(consulta) + 1)
                    if not db.ejecutar(
                        'INSERT INTO "SBODEMOAR"."' + str(fkValuesNO[
                            b]) + '" ("DocEntry","Code","U_CollCode","Canceled","Object","U_Active") VALUES ' +
                        "('" + str(maximoCollection) + "', '" + str(buscar) + "', '" + str(diccionarioTemporal[
                            'Collection']) + "', 'N', 'ARGNS_COLLECTION', 'Y')"):
                        errores = True
                elif 'Producer' == b:
                    if not db.ejecutar('INSERT INTO "SBODEMOAR"."' + fkValuesNO[b] + '" ("Code","Name","U_Active") VALUES ' +
                                "('" + str(buscar) + "', '" + str(buscar) + "', 'Y')"):
                        errores = True
                elif 'Division code' == b:
                    if not db.ejecutar('INSERT INTO "SBODEMOAR"."' + fkValuesNO[b] + '" ("Code","Name","U_Active") VALUES ' +
                                "('" + str(buscar) + "', '" + str(buscar) + "', 'Y')"):
                        errores = True
                elif 'Year' == b:
                    if not db.ejecutar('INSERT INTO "SBODEMOAR"."' + fkValuesNO[b] + '" ("Code","Name","U_Active") VALUES ' +
                                "('" + str(buscar) + "', '" + str(buscar) + "', 'Y')"):
                        errores = True
                log += '\nValue created.'

        # Si se ejecutó sin problemas, hacer el insert
        log += '\nAll correct, inserting model.'

        if diccionarioTemporal['Designer shoe'] != '' and diccionarioTemporal['Designer sole'] != '':
            query = """INSERT INTO "SBODEMOAR"."@ARGNS_MODEL" 
            ("U_DocNumb", "DataSource", "DocEntry", "Code", "Object", "U_ModCode", "U_ModDesc", "U_LineCode", "U_ModGrp", "U_ATGrp", "U_SapGrp", "U_Season", 
            "U_CollCode", "U_Brand", "U_Designer", "U_Owner", "U_Division", "U_Year", "U_COO", "U_Vendor", "U_MainWhs", 
            "U_PList", "U_Currency", "U_Price", "U_SclCode", "U_ChartCod")
            VALUES ( """ \
                    "'1', 'I',  '" + str(maximo) + "', " \
                                                   " '" + str(maximo) + "', 'ARGNS_MODEL', " \
                                                                        " '" + diccionarioTemporal['Code'] + "', " \
                                                                                                             " '" + \
                    diccionarioTemporal['Description'] + "', " \
                                                         " '" + diccionarioTemporal['Segment code'] + "', " \
                                                                                                      " '" + \
                    diccionarioTemporal['Group code'] + "', " \
                                                        " '" + codigo_segmentacion + "', " \
                                                                                     " '" + \
                    diccionarioTemporal['SAP Item Group'] + "', " \
                                                            " '" + diccionarioTemporal['Season'] + "', " \
                                                                                                   " '" + \
                    diccionarioTemporal['Collection'] + "', " \
                                                        " '" + diccionarioTemporal['Producer'] + "', " \
                                                                                                 " '" + \
                    diccionarioTemporal['Designer shoe'] + "', " \
                                                           " '" + diccionarioTemporal['Designer sole'] + "', " \
                                                                                                         " '" + \
                    diccionarioTemporal['Division code'] + "', " \
                                                           " '" + diccionarioTemporal['Year'] + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Country of Origin'] + "', " \
                                               " '" + str(vendedores[0]) + "', " \
                                                                      " '" + diccionarioTemporal['Main warehouse'] + "', " \
                                                                                                                     " '" + str(pkPriceList) + "', " \
                                                                                                                                          " '" + \
                    diccionarioTemporal['Currency'] + "', " \
                                                     " '" + str(diccionarioTemporal['Price']) + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Size Chart'] + "', " \
                                        " '')"
        elif diccionarioTemporal['Designer shoe'] == '' and diccionarioTemporal['Designer sole'] == '':
            query = """INSERT INTO "SBODEMOAR"."@ARGNS_MODEL" 
            ("U_DocNumb", "DataSource", "DocEntry", "Code", "Object", "U_ModCode", "U_ModDesc", "U_LineCode", "U_ModGrp", "U_ATGrp", "U_SapGrp", "U_Season", 
            "U_CollCode", "U_Brand", "U_Division", "U_Year", "U_COO", "U_Vendor", "U_MainWhs", 
            "U_PList", "U_Currency", "U_Price", "U_SclCode", "U_ChartCod")
            VALUES ( """ \
                    "'1', 'I',  '" + str(maximo) + "', " \
                                                   " '" + str(maximo) + "', 'ARGNS_MODEL', " \
                                                                        " '" + diccionarioTemporal['Code'] + "', " \
                                                                                                             " '" + \
                    diccionarioTemporal['Description'] + "', " \
                                                         " '" + diccionarioTemporal['Segment code'] + "', " \
                                                                                                      " '" + \
                    diccionarioTemporal['Group code'] + "', " \
                                                        " '" + codigo_segmentacion + "', " \
                                                                                     " '" + \
                    diccionarioTemporal['SAP Item Group'] + "', " \
                                                            " '" + diccionarioTemporal['Season'] + "', " \
                                                                                                   " '" + \
                    diccionarioTemporal['Collection'] + "', " \
                                                        " '" + diccionarioTemporal['Producer'] + "', '" + \
                    diccionarioTemporal['Division code'] + "', " \
                                                           " '" + diccionarioTemporal['Year'] + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Country of Origin'] + "', " \
                                               " '" + str(vendedores[0]) + "', " \
                                                                      " '" + diccionarioTemporal['Main warehouse'] + "', " \
                                                                                                                     " '" + str(pkPriceList) + "', " \
                                                                                                                                          " '" + \
                    diccionarioTemporal['Currency'] + "', " \
                                                     " '" + str(diccionarioTemporal['Price']) + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Size Chart'] + "', " \
                                        " '')"
        elif diccionarioTemporal['Designer shoe'] == '':
            query = """INSERT INTO "SBODEMOAR"."@ARGNS_MODEL" 
            ("U_DocNumb", "DataSource", "DocEntry", "Code", "Object", "U_ModCode", "U_ModDesc", "U_LineCode", "U_ModGrp", "U_ATGrp", "U_SapGrp", "U_Season", 
            "U_CollCode", "U_Brand", "U_Owner", "U_Division", "U_Year", "U_COO", "U_Vendor", "U_MainWhs", 
            "U_PList", "U_Currency", "U_Price", "U_SclCode", "U_ChartCod")
            VALUES ( """ \
                    "'1', 'I',  '" + str(maximo) + "', " \
                                                   " '" + str(maximo) + "', 'ARGNS_MODEL', " \
                                                                        " '" + diccionarioTemporal['Code'] + "', " \
                                                                                                             " '" + \
                    diccionarioTemporal['Description'] + "', " \
                                                         " '" + diccionarioTemporal['Segment code'] + "', " \
                                                                                                      " '" + \
                    diccionarioTemporal['Group code'] + "', " \
                                                        " '" + codigo_segmentacion + "', " \
                                                                                     " '" + \
                    diccionarioTemporal['SAP Item Group'] + "', " \
                                                            " '" + diccionarioTemporal['Season'] + "', " \
                                                                                                   " '" + \
                    diccionarioTemporal['Collection'] + "', " \
                                                        " '" + diccionarioTemporal['Producer'] + "', " \
                                                                                                 "" + \
                    " '" + diccionarioTemporal['Designer sole'] + "'," \
                                                                                                         " '" + \
                    diccionarioTemporal['Division code'] + "', " \
                                                           " '" + diccionarioTemporal['Year'] + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Country of Origin'] + "', " \
                                               " '" + str(vendedores[0]) + "', " \
                                                                      " '" + diccionarioTemporal['Main warehouse'] + "', " \
                                                                                                                     " '" + str(pkPriceList) + "', " \
                                                                                                                                          " '" + \
                    diccionarioTemporal['Currency'] + "', " \
                                                     " '" + str(diccionarioTemporal['Price']) + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Size Chart'] + "', " \
                                        " '')"
        else:
            query = """INSERT INTO "SBODEMOAR"."@ARGNS_MODEL" 
            ("U_DocNumb", "DataSource", "DocEntry", "Code", "Object", "U_ModCode", "U_ModDesc", "U_LineCode", "U_ModGrp", "U_ATGrp", "U_SapGrp", "U_Season", 
            "U_CollCode", "U_Brand", "U_Designer", "U_Division", "U_Year", "U_COO", "U_Vendor", "U_MainWhs", 
            "U_PList", "U_Currency", "U_Price", "U_SclCode", "U_ChartCod")
            VALUES ( """ \
                    "'1', 'I',  '" + str(maximo) + "', " \
                                                   " '" + str(maximo) + "', 'ARGNS_MODEL', " \
                                                                        " '" + diccionarioTemporal['Code'] + "', " \
                                                                                                             " '" + \
                    diccionarioTemporal['Description'] + "', " \
                                                         " '" + diccionarioTemporal['Segment code'] + "', " \
                                                                                                      " '" + \
                    diccionarioTemporal['Group code'] + "', " \
                                                        " '" + codigo_segmentacion + "', " \
                                                                                     " '" + \
                    diccionarioTemporal['SAP Item Group'] + "', " \
                                                            " '" + diccionarioTemporal['Season'] + "', " \
                                                                                                   " '" + \
                    diccionarioTemporal['Collection'] + "', " \
                                                        " '" + diccionarioTemporal['Producer'] + "', " \
                                                                                                 " '" + \
                    diccionarioTemporal['Designer shoe'] + "', " \
                                                           "'" + \
                    diccionarioTemporal['Division code'] + "', " \
                                                           " '" + diccionarioTemporal['Year'] + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Country of Origin'] + "', " \
                                               " '" + str(vendedores[0]) + "', " \
                                                                      " '" + diccionarioTemporal['Main warehouse'] + "', " \
                                                                                                                     " '" + str(pkPriceList) + "', " \
                                                                                                                                          " '" + \
                    diccionarioTemporal['Currency'] + "', " \
                                                     " '" + str(diccionarioTemporal['Price']) + "', " \
                                                                                                " '" + diccionarioTemporal[
                        'Size Chart'] + "', " \
                                        " '')"

        result = db.ejecutar(query)

        # Modificamos los UDF
        # Para modificar los UDF, primero necesitamos saber que columnas se estan utilizando, excluyendo las basicas del excel
        # En estas dos instrucciones obtenemos todas las cabeceras que sean UDFs de la linea actual (Solo las que tengan valores usandose)
        # (Si la columna UDF de la linea actual está en blanco, entonces no se trae)
        a = excelModels.iloc[line - 1].dropna().to_frame().index.values
        UDFexcel = [e for e in a if e not in cabeceras]

        # Nos aseguramos de que todos los UDF que necesita la fila existan en la base de datos
        # Para ello, primero nos fijamos cuales son los UDFs creados en la base de datos
        UDFbase = db.consultarArreglo(
            "SELECT COLUMN_NAME FROM SYS.COLUMNS C WHERE C.SCHEMA_NAME = 'SBODEMOAR' AND TABLE_NAME = '@ARGNS_MODEL' AND COLUMN_NAME LIKE 'U!_%' ESCAPE '!'")
        for UDF in UDFexcel:
            if ('U_' + UDF) not in UDFbase:
                raise Exception('UDF not found. (' + UDF + ')')
        log += '\nAll UDFs found in DataBase'

        for UDF in UDFexcel:
            query = 'UPDATE "SBODEMOAR"."@ARGNS_MODEL" '
            query += 'SET "' + str('U_' + UDF) + '" = ' + "'" + str(excelModels[str(UDF)][line - 1]) + "' WHERE "
            query += '"U_ModCode" = ' + "'" + diccionarioTemporal['Code'] + "'"
            resultUDF = db.ejecutar(query)

        log += '\nModel insertion successfully'
        if resultUDF and result and not errores:
            print('Line ' + str(line) + ' - Insertion OK (Models)')
            simpleLog += '\nLine ' + str(line) + ' - Insertion OK (Models)'
            # Accept equals to COMMIT
            db.accept()
        else:
            print("Houston, we've had a problem, reverting model " + diccionarioTemporal['Code'])
            simpleLog += '\nLine ' + str(line) + ' - ERROR (Models)'
            db.revert()
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        simpleLog += '\nLine ' + str(line) + ' - ERROR (Models)'
        log += '\nAn exception has occurred: ' + str(e)
        print('An exception has occurred: ' + str(e) + '. Line ' + str(line_number))
        db.revert()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES SKU ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TODO Cambiar la columna SKUGEN
# TODO implementar cambios guardados en la compu

cabeceras = 'Model code', 'SKU', 'EAN -Barcode Item Master Data'
line = 0
for a in range(len(excelSku)):
    line += 1
    log += '\n\nEXCEL LINE ' + str(line) + ' - SKUs\n'
    try:
        # La fila actual es una lista que tiene el Model Code, el SKU y el Codigo de Barras
        filaActual = [excelSku['Model code'][a], excelSku['SKU'][a], excelSku['EAN -Barcode Item Master Data'][a]]

        # Antes de seguir, checkeamos que el modelo exista en la base de datos
        respuesta = db.consultar('SELECT 1 FROM "SBODEMOAR"."@ARGNS_MODEL" WHERE "U_ModCode" = ' + "'" + filaActual[0] + "'")
        if '1' not in respuesta:
            raise Exception('Model "' + filaActual[0] + '" doesnt exists for SKU "' + filaActual[1] + "'")

        color = filaActual[1].split('-')[-2]
        talle = filaActual[1].split('-')[-1]

        queryTemporal = 'SELECT "U_ModDesc", "U_SapGrp", "U_SclCode", "U_COO", "U_Division", "U_Season", "U_Year" ' \
                        'FROM "SBODEMOAR"."@ARGNS_MODEL" WHERE "U_ModCode" ='
        queryTemporal += "'" + filaActual[0] + "'"
        modeloTemporal = db.consultarArreglo(queryTemporal)
        modelo = []
        for b in modeloTemporal:
            if b != ' ':
                modelo.append(b)

        result = conexionServicio.insertSku(filaActual[1], filaActual[0], color, filaActual[0], modeloTemporal[2], talle,
                                   modeloTemporal[3], modeloTemporal[6], modeloTemporal[4], modeloTemporal[5], filaActual[2])
        if result == False:
            raise Exception('Insertion error: SKU "' + filaActual[0] + '", Model "' + filaActual[1] + '"')
        else:
            simpleLog += '\nCorrect - Line ' + str(line) + ' from SKUs (SKU: "' + excelSku['SKU'][a] + '", MODEL: "' + excelSku['Model code'][a] + '")'
            log += '\nCorrect - Line ' + str(line) + ' from SKUs (SKU: "' + excelSku['SKU'][
                a] + '", MODEL: "' + excelSku['Model code'][a] + '")'
            print('Correct - Line ' + str(line) + ' from SKUs (SKU: "' + excelSku['SKU'][a] + '", MODEL: "'
                  + excelSku['Model code'][a] + '")')
    except Exception as e:
        db.revert()
        simpleLog += '\nError at line ' + str(line) + ' from SKUs'
        log += '\nAn exception has occurred: ' + str(e)
        print('An exception has occurred: ' + str(e))


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                      --- INSTRUCCIONES PREPACKS ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES DEL LOG ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

print('Saving log...')
# Mensaje en el log
f = open(logPath, "a")
f.write(log)
f.close()

fs = open(simpleLogPath, "a")
fs.write(simpleLog)
fs.close()

# Show log
#print('Showing log')
#print(log)

input('OK...')