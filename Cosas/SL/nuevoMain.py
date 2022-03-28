import sys
from dataBase import BaseDatos
import pandas as pd
import datetime
import numpy as np
from SapServiceLayer import SapSL
import time

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                  --- DEFINICIONES ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Ruta del log y la variable del log
logPath = 'C:\\Users\\Administrator\\Desktop\\log.txt'
log = '\n\nScript execution - ' + str(datetime.datetime.now())

# Ruta de los archivos
mainPath = 'C:\\Users\\Administrator\\Desktop\\main.csv'
skuPath = 'C:\\Users\\Administrator\\Desktop\\sku.csv'
prepacksPath = 'C:\\Users\\Administrator\\Desktop\\prepacks.csv'

# Direccion de la Base de Datos
direccion = '10.52.104.115'
puerto = '30015'
usuario = 'B1ADMIN'
clave = 'Inn0vate2021'

# Parametros ServiceLayer
URL = "https://10.52.104.115:50000/b1s/v1/"
dataBase = "ASTOR_MULLER_GERMANY"
userName = "manager"
password = "Man#1234"

# Variables
todoBien = True

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
excelModels = pd.read_csv(mainPath, dtype=np.str_)
excelSku = pd.read_csv(skuPath, dtype=np.str_)
excelPrepacks = pd.read_csv(prepacksPath, dtype=np.str_)
log += '\nFile read'

# Cabeceras del excel que no son UDFs
cabeceras = 'Code', 'Description', 'Segment code', 'Segment', 'Group code', 'Group', 'AF Segmentation', \
            'SAP Item Group', 'Season', 'Collection code', 'Collection', 'Producer', 'Designer shoe', 'Designer sole', \
            'Division code', 'Year', 'Country of Origin', 'Vendor', 'Main warehouse', 'Price List', 'Currency', \
            'Price', 'Size Chart', 'Color Code'

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES MODELOS ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

log += '\nStarting...\n'
lineasConErrorModel = []

# Checkeamos la existencia de los UDFs, caso contrario, se crean
log += '\nChecking UDFs.'
listaTemporal = excelModels.iloc[0].to_frame().index.values
columnasNuevas = [e for e in listaTemporal if e not in cabeceras]
udfsNuevos, udfsExistentes, udfsConError = conexionServicio.asegurar_udf(columnasNuevas)
log += '\nExisting UDFs: ' + str(udfsExistentes)
log += '\nCreated UDFs: ' + str(udfsNuevos)
log += '\nERROR UDFs: ' + str(udfsConError)

c = 0
c100 = 0
print('Model row N. 0')
for nlinea in range(len(excelModels)):
    # Esto sirve para saber hasta que punto hay que revertir cuando algo salga mal.
    # 0 = Inicio y checkeos previos (No hay que revertir nada)
    # 1 = No se pudieron insertar o relacionar los valores (Excluyendo vendors)
    # 2 = No se pudieron relacionar los vendors
    cadena = {}
    etapa = 0
    c += 1
    c100 += 1
    if c == 10:
        time.sleep(2)
        print('Model row N. ' + str(nlinea + 1))
        c = 0
    if c100 == 100:
        print('Reconnecting to ServiceLayer')
        conexionServicio = None
        time.sleep(5)
        c100 = 0
        conexionServicio = SapSL(URL, dataBase, userName, password)
        if not conexionServicio.connectedStatus():
            log += '\nFatal error: No connection with Sap ServiceLayer...'
            f = open(logPath, "a")
            f.write(log)
            f.close()
            print(log)
            exit()
        log += '\nReconnected to Sap Service Layer'

    filaActual = excelModels.iloc[nlinea]
    log += '\n\nEXCEL LINE ' + str(nlinea + 1) + ' - MODELS'

    try:
        # Primero verificamos que el modelo no exista previamente
        if conexionServicio.existe_modelo(filaActual['Code']):
            log += '\nModel "' + filaActual['Code'] + '" already exists. Skipped'
            raise Exception('Model already exists in ARGNS_MODEL')
        log += '\nModel "' + filaActual['Code'] + '" doesnt exists. Proceeding.'

        # Verificamos que los campos que tienen que existir si o si en la base de datos lo hagan. Estos NO se deben crear.
        if not conexionServicio.asegurar_existencia(filaActual['SAP Item Group'], filaActual['Designer shoe'],
                                                    filaActual['Designer sole'], filaActual['Vendor'],
                                                    filaActual['Main warehouse'], filaActual['Price List'],
                                                    filaActual['Currency']):
            log += '\nNot all critical values found. Model "' + filaActual['Code'] + '". Skipped'
            raise Exception('Not all critical values found. Model "' + filaActual['Code'] + '". Skipped')
        log += '\nAll critical values found. Model "' + filaActual['Code'] + '". Proceeding with not critical values.'

        # Obtenemos el codigo identificador que va a tener que tener nuestro nuevo modelo
        #identificador = db.siguienteCode('"' + dataBase + '"."@ARGNS_MODEL"')
        identificador = db.siguienteCodeNew(dataBase, "@ARGNS_MODEL")

        # Verificamos que los campos no criticos existan. Caso contrario, se deben crear.
        # productLineCode, productLineName, productGroupCode, productGroupName, AFsegmentation, season, collectionCode,
        # brand, division, year, sizeChart, color
        status, cadena = conexionServicio.asegurar_o_crear(db, filaActual['Segment code'], filaActual['Segment'],
                                                           filaActual['Group code'],
                                                           filaActual['Group'], filaActual['AF Segmentation'],
                                                           filaActual['Season'],
                                                           filaActual['Collection code'], filaActual['Producer'],
                                                           filaActual['Division code'], filaActual['Year'],
                                                           filaActual['Size Chart'],
                                                           filaActual['Color Code'])
        etapa = 1
        if status:
            log += '\nExisting values: ' + str(cadena[0])
            log += '\nCreated values: ' + str(cadena[1])
        else:
            log += '\nError: ' + str(cadena)
            raise Exception('Error: ' + str(cadena))

        # Relacionamos los vendedores con el modelo en la tabla MODVENDOR
        #NOMBRADO PARA PRUEBA - AGU
        respuesta, relacionados = conexionServicio.relateVendors(db, str(filaActual['Code']), str(filaActual['Vendor']))
        etapa = 2
        if respuesta:
            log += '\nCorrectly related vendors. ' + str(relacionados)
        else:
            log += '\nError relating vendors. Only could relate ' + str(relacionados)
            raise Exception('Vendor couldnt be related with model')

        # Insertamos el modelo, para ello primero armamos el diccionario con los colores
        colores = filaActual['Color Code'].strip().split(';')
        cuerpoColores = []
        for color in colores:
            cuerpoColores.append({"Code": identificador, "U_ColCode": color})

        # Luego armamos el diccionario con los sizes
        codigosSize = db.consultarFilas(
            'SELECT "U_SizeCode" FROM "' + dataBase + '"."@ARGNS_SIZE" WHERE "Code" = ' + "'" + db.consultaElemento(
                '"' + dataBase + '"."@ARGNS_SCALE"', 'U_SclCode', filaActual['Size Chart'], 'Code').strip().split(' ')[0] + "'")
        cuerpoCodigosSize = []
        for size in codigosSize:
            cuerpoCodigosSize.append(
                {"Code": identificador, "U_SclCode": filaActual['Size Chart'], "U_SizeCod": size[0]})

        # Luego armamos el diccionario con los UDFs
        udfs = {}
        for columnaUDF in columnasNuevas:
            if str(filaActual[columnaUDF]) != 'nan':
                udfs['U_ARGNS_' + columnaUDF.replace(" ", "_")] = filaActual[columnaUDF]

        # Y finalmente insertamos
        cuerpo = {"Code": str(identificador),
                  "Name": str(filaActual['Code']),
                  "U_ATGrp": conexionServicio.consulta('ARGNS_APPTEXGRPS', 'Name', str(filaActual['AF Segmentation']),
                                                       'Code'),
                  "U_ModCode": str(filaActual['Code']),
                  "U_ModDesc": str(filaActual['Description']),
                  "U_Year": db.consultaElemento('"' + dataBase + '"."@ARGNS_YEAR"', 'U_Year', str(filaActual['Year']),
                                                'Code').strip(),
                  "U_COO": str(filaActual['Country of Origin']),
                  "U_SapGrp": str(filaActual['SAP Item Group']),
                  "U_PList": str(
                      conexionServicio.consulta('PriceLists', 'PriceListName ', filaActual['Price List'].strip(),
                                                'PriceListNo')),
                  "U_Division": str(filaActual['Division code']),
                  "U_Season": str(filaActual['Season']),
                  "U_FrgnDesc": str(filaActual['Description']),
                  "U_ModGrp": db.consultaElemento('"' + dataBase + '"."@ARGNS_MODELGRP"', 'Code',
                                                  str(filaActual['Group code']), 'Code').strip(),
                  "U_Designer": str(filaActual['Designer shoe']),
                  "U_SclCode": str(filaActual['Size Chart']),
                  "U_LineCode": str(filaActual['Segment code']),
                  "U_Vendor": str(((filaActual['Vendor']).strip().split(';'))[0]),
                  "U_MainWhs": str(filaActual['Main warehouse']),
                  "U_Currency": str(filaActual['Currency']),
                  "U_Owner": str(filaActual['Designer sole']),
                  "U_Price": str(filaActual['Price']),
                  "U_CollCode": str(filaActual['Collection code']),
                  "U_Brand": str(filaActual['Producer']),
                  "U_DocNumb": "1", "ARGNS_MODEL_COLORCollection": cuerpoColores,
                  "ARGNS_MODEL_SIZECollection": cuerpoCodigosSize}
        listaEliminar = []
        for atributoCuerpo in cuerpo:
            if cuerpo[atributoCuerpo] == 'nan' or cuerpo[atributoCuerpo] == '':
                listaEliminar.append(atributoCuerpo)
        for atributoCuerpo in listaEliminar:
            del cuerpo[atributoCuerpo]

        cuerpo.update(udfs)

        # Esperamos un segundo porque el ServiceLayer es super fragil y se rompe si mandamos muchas solicitudes rapido
        time.sleep(1)
        respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
        if respuestaModelo == 'e' or not respuestaModelo:
            log += '\nError inserting MODEL. Attempt 1: ' + str(cuerpo).replace("'", '"')
            time.sleep(1)
            respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
            if respuestaModelo == 'e' or not respuestaModelo:
                log += '\nError inserting MODEL. Attempt 2: ' + str(cuerpo).replace("'", '"')
                respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                if respuestaModelo == 'e' or not respuestaModelo:
                    log += '\nError inserting MODEL. Attempt 3: ' + str(cuerpo).replace("'", '"')
                    time.sleep(2)
                    respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                    if respuestaModelo == 'e' or not respuestaModelo:
                        log += '\nError inserting MODEL. Attempt 4: ' + str(cuerpo).replace("'", '"')
                        time.sleep(2)
                        respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                        if respuestaModelo == 'e' or not respuestaModelo:
                            log += '\nError inserting MODEL. Attempt 5: ' + str(cuerpo).replace("'", '"')
                            respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                            if respuestaModelo == 'e' or not respuestaModelo:
                                log += '\nError inserting MODEL. Attempt 6: ' + str(cuerpo).replace("'", '"')
                                time.sleep(3)
                                respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                                if respuestaModelo == 'e' or not respuestaModelo:
                                    log += '\nError inserting MODEL. Attempt 7: ' + str(cuerpo).replace("'", '"')
                                    respuestaModelo = conexionServicio.insertar_modelo(str(cuerpo).replace("'", '"'))
                                    if respuestaModelo == 'e' or not respuestaModelo:
                                        log += '\nError inserting MODEL. Attempt 8: ' + str(cuerpo).replace("'", '"')
                                        respuestaModelo = conexionServicio.insertar_modelo(
                                            str(cuerpo).replace("'", '"'))
                                        if respuestaModelo == 'e' or not respuestaModelo:
                                            log += '\nError inserting MODEL. Attempt 9: ' + str(cuerpo).replace("'",'"')
                                            time.sleep(4)
                                            respuestaModelo = conexionServicio.insertar_modelo(
                                                str(cuerpo).replace("'", '"'))
                                            if respuestaModelo == 'e' or not respuestaModelo:
                                                log += '\nError inserting MODEL. Attempt 10: ' + str(cuerpo).replace("'",'"')
                                                raise Exception('Error inserting MODEL')
        log += '\nModel "' + str(filaActual['Code']) + '" inserted correctly.'
        print('Model "' + str(filaActual['Code']) + '" inserted correctly.')
        log += '\nRequest executed: ' + str(cuerpo)


    except Exception as e:
        lineasConErrorModel.append(nlinea + 1)
        log += '\nException: ' + str(e)
        print('Exception: ' + str(e))
        if etapa == 0:
            pass
        elif etapa == 1:
            # conexionServicio.eliminarCreados(db, cadena[1])
            pass
        elif etapa == 2:
            # conexionServicio.eliminarCreados(db, cadena[1])
            db.ejecutar('DELETE FROM "' + dataBase + '"."@ARGNS_MODVENDOR" WHERE "Code" = ' + "'" + str(
                filaActual['Code']).strip() + "'")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES SKUs ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Checkeamos la existencia de los UDFs, caso contrario, se crean
log += '\n\n\nChecking UDFs.'
udfsNuevos, udfsExistentes, udfsConError = conexionServicio.asegurar_udf_oitm(columnasNuevas)
log += '\nExisting UDFs: ' + str(udfsExistentes)
log += '\nCreated UDFs: ' + str(udfsNuevos)
log += '\nERROR UDFs: ' + str(udfsConError)

lineasConErrorSKU = []
c = 0
c100 = 0
print('SKU row N. 0')
for nLinea in range(len(excelSku)):
    c += 1
    if c == 25:
        time.sleep(2)
        print('SKU row N. ' + str(nLinea + 1))
        c = 0
    if c100 == 100:
        print('Reconnecting to ServiceLayer')
        conexionServicio = None
        time.sleep(5)
        c100 = 0
        conexionServicio = SapSL(URL, dataBase, userName, password)
        if not conexionServicio.connectedStatus():
            log += '\nFatal error: No connection with Sap ServiceLayer...'
            f = open(logPath, "a")
            f.write(log)
            f.close()
            print(log)
            exit()
        log += '\nReconnected to Sap Service Layer'

    try:
        log += '\n\nEXCEL LINE ' + str(nLinea + 1) + ' - SKUs'
        filaActual = {'Model': excelSku['Model code'][nLinea], 'SKU': excelSku['SKU'][nLinea],
                      'BarCode': excelSku['EAN -Barcode Item Master Data'][nLinea]}
        color = filaActual['SKU'].split('-')[-2]
        talle = filaActual['SKU'].split('-')[-1]

        # Primero checkeamos que el modelo exista en la base de datos
        existe = conexionServicio.existe('ARGNS_MODEL', 'U_ModCode', filaActual['Model'])
        if not existe:
            log += '\nError inserting SKU. Model doesnt exists.'
            lineasConErrorSKU.append(str(nLinea + 1))
            continue

        # Traemos los datos del modelo correspondiente para poder insertar el SKU
        queryTemporal = 'SELECT "U_ModDesc", "U_SapGrp", "U_SclCode", "U_COO", "U_Division", "U_Season", "U_Year" , "Code"' \
                        'FROM "' + dataBase + '"."@ARGNS_MODEL" WHERE "U_ModCode" ='
        queryTemporal += "'" + filaActual['Model'] + "'"
        modeloTemporal = db.consultarArreglo(queryTemporal)
        modelo = []
        for b in modeloTemporal:
            if b != ' ':
                modelo.append(b)

        # Traemos los udfs
        udfs = {}
        for udf in columnasNuevas:
            try:
                respuestaConsulta = conexionServicio.consulta('ARGNS_MODEL', "U_ModCode", filaActual['Model'], "U_" + udf)
                if str(respuestaConsulta) != 'None':
                    udfs["U_ARGNS_" + udf.replace(" ", "_")] = respuestaConsulta
            except Exception:
                pass

        result = False
        cortar = 0
        limite = 4  # Cuantos intentos se van a hacer hasta dejar de intentar insertar el sku
        while not result:
            cortar += 1
            log += '\nAttempt' + str(cortar)
            result = conexionServicio.insertSku(filaActual['SKU'], filaActual['Model'], color, filaActual['Model'],
                                                modeloTemporal[2], talle,
                                                modeloTemporal[3], modeloTemporal[6], modeloTemporal[4], modeloTemporal[5],
                                                filaActual['BarCode'], udfs)
            if cortar > limite: break
        if not result:
            lineasConErrorSKU.append(str(nLinea + 1))
            log += '\nError inserting SKU "' + filaActual['SKU'] + '"'
        else:
            log += '\nCorrect - Line ' + str(nLinea + 1) + ' from SKUs (SKU: "' + excelSku['SKU'][nLinea] + '", MODEL: "' + \
                   excelSku['Model code'][nLinea] + '")'
            print('SKU inserted correctly.')
            # Cambiamos el estado del modelo para que diga que tiene generado un SKU
            conexionServicio.cambiarEstadoSKU(modeloTemporal[7])

    except Exception:
        lineasConErrorSKU.append(str(nLinea + 1))
        log += '\nError inserting SKU at line ' + str(nLinea + 1)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                       --- INSTRUCCIONES PREPACKs ---
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

print('PREPACK row N. 0')
c = 0
c100 = 0
for nLinea in range(len(excelPrepacks)):
    c += 1
    if c == 25:
        time.sleep(2)
        print('PREPACK row N. ' + str(nLinea + 1))
        c = 0
    if c100 == 100:
        print('Reconnecting to ServiceLayer')
        conexionServicio = None
        time.sleep(5)
        c100 = 0
        conexionServicio = SapSL(URL, dataBase, userName, password)
        if not conexionServicio.connectedStatus():
            log += '\nFatal error: No connection with Sap ServiceLayer...'
            f = open(logPath, "a")
            f.write(log)
            f.close()
            print(log)
            exit()
        log += '\nReconnected to Sap Service Layer'
    try:
        log += '\n\nEXCEL LINE ' + str(nLinea + 1) + ' - PREPACKs'
        #filaActual = {'Model': excelSku['Model code'][nLinea], 'SKU': excelSku['SKU'][nLinea],
        #              'BarCode': excelSku['EAN -Barcode Item Master Data'][nLinea]}

        if conexionServicio.existe('ARGNS_PREPACK', 'U_PpCode', excelPrepacks['Prepack code'][nLinea]):
            raise Exception('Prepack Code already exists (' + excelPrepacks['Prepack code'][nLinea] + ')')


        resultado = conexionServicio.insertar_prepack(db, excelPrepacks['Prepack code'][nLinea],
                                                         excelPrepacks['Description'][nLinea],
                                                         excelPrepacks['Model code'][nLinea],
                                                         excelPrepacks['Segmentation'][nLinea],
                                                         excelPrepacks['Model color'][nLinea],
                                                         excelPrepacks['Warehouse'][nLinea],
                                                      str(
                                                          conexionServicio.consulta('PriceLists', 'PriceListName ',
                                                                                    excelPrepacks['Price List'][nLinea].strip(),
                                                                                    'PriceListNo')),
                                                         excelPrepacks['Scale'][nLinea],
                                                         excelPrepacks['SizeRun'][nLinea],
                                                         excelPrepacks['EAN'][nLinea])
        if resultado == True:
            log += '\nPrepack inserted correctly.'
        else:
            log += '\nError inserting Prepack.'
    except Exception as e:
        log += '\nError inserting Prepack. (' + str(e) + ').'


# Parte final del log
log += '\n\nLines from MODELS with errors: ' + str(lineasConErrorModel)
log += '\n\nLines from SKUs with errors: ' + str(lineasConErrorSKU)

print(log)

archivoSalida = open(logPath, 'a')
archivoSalida.write(log)
archivoSalida.close()
