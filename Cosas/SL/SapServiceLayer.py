import requests
import urllib3
from dataBase import BaseDatos
import json


# Desactivamos warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SapSL():
    def __init__(self, url, database, username, password):
        try:
            self.URL = url
            self.dataBase = database
            self.userName = username
            self.password = password

            # Inicializamos los datos
            self.datos = '{"CompanyDB": "' + self.dataBase + '", "UserName": "' + self.userName + '", "Password": "' + self.password + '"}'

            # Iniciamos sesion y traemos la RouteID y la SessionID
            r = requests.post(self.URL + 'Login', data=self.datos, verify=False)
            self.sessionId = r.cookies.get('B1SESSION')
            self.routeId = r.cookies.get('ROUTEID')

            cookie = 'CompanyDB=' + self.dataBase + '; B1SESSION=' + self.sessionId + '; ROUTEID=' + self.routeId
            self.headers = {'Cookie': cookie, 'cookie': cookie}
            self.roto = False
        except Exception as e:
            print(e)
            self.roto = True

    def connectedStatus(self):
        if self.roto:
            return False
        return True

    # Le decimos que tipo de objeto queremos obtener y su identificacion, y nos dice si existe (True) o no (False)
    def existe(self, objeto, atributoNombre, atributo):
        URL = self.URL + objeto + "?$filter=" + atributoNombre + " eq '" + atributo + "'"
        r = requests.get(URL, verify=False, headers=self.headers)
        data = r.json()
        if 'error' in data or ('value' in data and not data['value']):
            return False
        else:
            return True

    # Lo mismo que antes pero con enteros
    def existeInt(self, objeto, atributoNombre, atributo):
        URL = self.URL + objeto + "?$filter=" + atributoNombre + " eq " + atributo + ""
        r = requests.get(URL, verify=False, headers=self.headers)
        data = r.json()
        if 'error' in data or ('value' in data and not data['value']):
            return False
        else:
            return True

    def insercion(self, tabla, cuerpo):
        URL = self.URL + tabla
        r = requests.post(URL, data=cuerpo, verify=False, headers=self.headers)
        data = r.json()
        if 'error' in data and (data['error']['code'] != -2035 and data['error']['code'] != -5002):
            return False
        elif 'error' in data and data['error']['code'] == -5002:
            return 'a'
        elif 'error' in data and data['error']['code'] == -2035:
            return 'e'
        else:
            return True

    # Le damos el nombre de la tabla, y una clave primaria junto con su valor, para que nos devuelva otro valor de ese
    # mismo objeto todo
    def consulta(self, tabla, atributoEntradaNombre, atributoEntrada, atributoRetornarNombre):
        URL = self.URL + tabla + "?$filter=" + atributoEntradaNombre + " eq '" + atributoEntrada + "'"
        r = requests.get(URL, verify=False, headers=self.headers)
        data = r.json()
        if 'error' in data or ('value' in data and not data['value']):
            return False
        else:
            return data['value'][0][atributoRetornarNombre]

    def eliminar(self, tabla, clavePrimaria):
        URL = self.URL + tabla + "('" + clavePrimaria + "')"
        requests.delete(URL, verify=False, headers=self.headers)

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #                                       --- Funciones Modelos ---
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Checkear si un modelo especifico existe
    def existe_modelo(self, modelo):
        return self.existe('ARGNS_MODEL', 'U_ModCode', modelo)

    # Aca van los campos que tienen que existir si o si en la base de datos. No se deben crear.
    def asegurar_existencia(self, itemGroup, designerShoe, designerSole, vendorsRaw, warehouse, priceList, currency):
        itemGroup, designerShoe, designerSole, vendorsRaw, warehouse, priceList, currency = \
            str(itemGroup), str(designerShoe), str(designerSole), str(vendorsRaw), str(warehouse), str(priceList), \
            str(currency)
        if not self.existeInt('ItemGroups', 'Number', itemGroup):
            print('ItemGroups')
            return False
        if designerShoe != 'nan':
            if not self.existeInt('EmployeesInfo', 'EmployeeID', designerShoe):
                print('EmployeesInfo')
                return False
        if designerSole != 'nan':
            if not self.existeInt('Users', 'InternalKey', designerSole):
                print('Users')
                return False
        vendors = vendorsRaw.replace(' ', '').split(';')
        for vendor in vendors:
            if not self.existe('BusinessPartners', 'CardCode', vendor):
                print('BusinessPartners')
                return False
        if not self.existe('Warehouses', 'WarehouseCode', warehouse):
            print('Warehouses')
            return False
        if not self.existe('PriceLists', 'PriceListName', priceList):
            print('PriceLists')
            return False
        if not self.existe('Currencies', 'Code', currency):
            print('Currencies')
            return False
        return True

    # Aca van los campos que pueden o no existir, y en caso de que no lo hagan, hay que crearlos
    def asegurar_o_crear(self, db: BaseDatos, productLineCode, productLineName, productGroupCode, productGroupName,
                         AFsegmentation,
                         season, collectionCode, brand, division, year, sizeChart, color):
        createdItems = {}
        existingItems = {}

        # Los que se meten a la base de datos a traves de ServiceLayer es porque son UDOs y eso esta permitido
        # Los que se meten directamente a la base de datos es porque no se pueden introducir a traves de ServiceLayer

        # - PRODLINE -
        if self.existe('ARGNS_PRODLINE', 'Code', productLineCode):
            if not self.consulta('ARGNS_PRODLINE', 'Code', productLineCode, 'Name').strip() == productLineName.strip():
                return False, (
                            'Prodline "' + productLineCode + '-' + productLineName + '" already exists with another code')
            else:
                existingItems['productLineCode'] = productLineCode
                existingItems['productLineName'] = productLineName
        else:
            cuerpo = '{"Code": "' + productLineCode + '", "Name": "' + productLineName + '"}'
            if not self.insercion('ARGNS_PRODLINE', cuerpo):
                return False, 'Error inserting PRODLINE'
            else:
                createdItems['productLineCode'] = productLineCode
                createdItems['productLineName'] = productLineName

        # - PRODUCTGROUP -
        if db.existe('"' + self.dataBase + '"."@ARGNS_MODELGRP"', 'Code', productGroupCode):
            if not db.consultaElemento('"' + self.dataBase + '"."@ARGNS_MODELGRP"', 'Code', productGroupCode,
                                       'Name').strip() == productGroupName:
                return False, (
                            'ProdGroup "' + productGroupCode + '-' + productGroupName + '" already exists with another code')
            else:
                existingItems['productGroupCode'] = productGroupCode
                existingItems['productGroupName'] = productGroupName
        else:
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_MODELGRP" ("Code", "Name", "U_NFRCode", "U_Active")'
            query += " VALUES ('" + productGroupCode + "', '" + productGroupName + "', null, 'Y')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, 'Error inserting MODELGRP'
            else:
                createdItems['productGroupCode'] = productGroupCode
                createdItems['productGroupName'] = productGroupName
                db.accept()

        # - AFSegmentation -
        existe = self.existe('ARGNS_APPTEXGRPS', 'Name', AFsegmentation)
        if existe:
            existingItems['AFsegmentation'] = AFsegmentation
        else:
            siguiente = db.siguienteCode('"' + self.dataBase + '"."@ARGNS_APPTEXGRPS"')
            intento = self.insercion('ARGNS_APPTEXGRPS',
                                     '{"Code": "' + siguiente + '", "Name": "' + AFsegmentation + '", "U_UseMod": "Y", "U_UseCol": "Y","U_UseScl": "Y", "U_ModLen": 21, "U_ColLen": 21,"U_SizeLen": 5, "U_Active": "Y", "U_Sep": "-", "U_Model": "NoDesc","U_Color": "NoDesc","U_Scale": "NoDesc","U_Size": "NoDesc"}')
            if intento:
                createdItems['AFsegmentation'] = AFsegmentation
            else:
                return False, 'Error inserting AFsegmentation'

        # - Season -
        if db.existe('"' + self.dataBase + '"."@ARGNS_SEASON"', 'Code', season) or db.existe('"' + self.dataBase + '"."@ARGNS_SEASON"', 'Code', season):
            existingItems['season'] = season
        else:
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_SEASON" ("Code", "Name", "U_Active")'
            query += " VALUES ('" + season + "', '" + season + "', 'Y')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, 'Error inserting SEASON'
            else:
                createdItems['season'] = season
                db.accept()

        # - collectionCode -
        existe = self.existe('ARGNS_COLLECTION', 'Name', collectionCode)
        if existe:
            existingItems['collectionCode'] = collectionCode
        else:
            siguiente = db.siguienteCode('"' + self.dataBase + '"."@ARGNS_COLLECTION"')
            intento = self.insercion('ARGNS_COLLECTION',
                                     '{"Code": "' + siguiente + '","Name": "' + collectionCode + '","U_Season": "' + season + '","U_CollCode": "' + collectionCode + '"}')
            if intento:
                createdItems['collectionCode'] = collectionCode
            else:
                return False, 'Error inserting collectionCode'

        # - brand -
        if db.existe('"' + self.dataBase + '"."@ARGNS_BRAND"', 'Code', brand):
            existingItems['brand'] = brand
        else:
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_BRAND" ("Code", "Name", "U_Active")'
            query += " VALUES ('" + brand + "', '" + brand + "', 'Y')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, 'Error inserting BRAND'
            else:
                createdItems['brand'] = brand
                db.accept()

        # - division -
        if db.existe('"' + self.dataBase + '"."@ARGNS_DIV"', 'Code', division):
            existingItems['division'] = division
        else:
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_DIV" ("Code", "Name", "U_Active")'
            query += " VALUES ('" + division + "', '" + division + "', 'Y')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, 'Error inserting DIVISION'
            else:
                createdItems['division'] = division
                db.accept()

        # - year -
        siguiente = db.siguienteCode('"' + self.dataBase + '"."@ARGNS_YEAR"')
        if db.existe('"' + self.dataBase + '"."@ARGNS_YEAR"', 'U_Year', year):
            existingItems['year'] = year
        else:
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_YEAR" ("Code", "Name", "U_Year", "U_Active")'
            query += " VALUES ('" + siguiente + "', '" + year + "', '" + year + "', 'Y')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, 'Error inserting YEAR'
            else:
                createdItems['year'] = year
                db.accept()

        # - sizeChart -
        existe = self.existe('ARGNS_SCALE', 'U_SclCode', sizeChart)
        if existe:
            existingItems['sizeChart'] = sizeChart
        else:
            return False, 'SIZECHART "' + sizeChart + '" doesnt exists'

        # - color -
        colors = color.strip().split(';')
        createdColors = []
        existingColors = []
        for uniqueColor in colors:
            if not self.existe('ARGNS_COLOR', 'U_ColCode', uniqueColor):
                intento = self.insercion('ARGNS_COLOR',
                                     '{"Code": "' + uniqueColor + '","Name": "' + uniqueColor + '", "U_ColCode": "' + uniqueColor + '", "U_ColDesc": "' + uniqueColor + '"}')
                if intento:
                    createdColors.append(uniqueColor)
                elif not intento:
                    return False, 'Error inserting COLOR'
            else:
                existingColors.append(uniqueColor)
        existingItems['color'] = existingColors
        createdItems['color'] = createdColors

        return True, [existingItems, createdItems]

    def relateVendors(self, db: BaseDatos, modelCode: str, vendors: str):
        # - Relation with vendors -
        # Los vendors necesitan ser relacionados en la tabla MODVENDOR
        vendorsRelated = []
        vendors = vendors.strip().split(';')
        c = 0
        for vendor in vendors:
            identificadorActual = db.siguienteCode('"' + self.dataBase + '"."@ARGNS_MODVENDOR"')
            vendorName = db.consultaElemento('"' + self.dataBase + '"."OCRD"', 'CardCode', vendor, 'CardName').strip()
            c += 1
            query = 'INSERT INTO "' + self.dataBase + '"."@ARGNS_MODVENDOR" ("Code", "Name", "U_ModCode", "U_CardCode", "U_CardName", "U_CardType", "U_DefBP") VALUES ('
            if c == 1:
                query += "'" + identificadorActual + "', '" + identificadorActual \
                         + "', '" + modelCode + "', '" + vendor + "', '" + vendorName + "', 'S', 'Y')"
            else:
                query += "'" + identificadorActual + "', '" + identificadorActual \
                         + "', '" + modelCode + "', '" + vendor + "', '" + vendorName + "', 'S', 'N')"
            respuesta = db.ejecutar(query)
            if not respuesta:
                db.revert()
                return False, vendorsRelated
            else:
                db.accept()
                vendorsRelated.append(vendor)
        return True, vendorsRelated

    # Nos aseguramos de que todos los udf necesarios existan, y en caso contrario se los crea (se crea la columna en
    # la base de datos)
    def asegurar_udf(self, listaUDFs):
        udfsNuevos = []
        udfsExistentes = []
        udfsConError = []
        for udfSingle in listaUDFs:
            udf = ('ARGNS_' + udfSingle).replace(" ", "_")
            cuerpo = '{"Name": "' + udf + '","Description": "' + udf + '","Type": "db_Alpha", "Size": 100,"EditSize": 100, "TableName": "@ARGNS_MODEL"}'
            intento = self.insercion('UserFieldsMD', cuerpo)
            if intento == 'e' or intento == 'a':
                udfsExistentes.append(udf)
            elif intento:
                udfsNuevos.append(udf)
            elif not intento:
                udfsConError.append(udf)
        return udfsNuevos, udfsExistentes, udfsConError

    # Nos aseguramos de que todos los udf necesarios existan, y en caso contrario se los crea (se crea la columna en
    # la base de datos)
    def asegurar_udf_oitm(self, listaUDFs):
        udfsNuevos = []
        udfsExistentes = []
        udfsConError = []
        for udfSingle in listaUDFs:
            udf = udfSingle.replace(" ", "_")
            cuerpo = '{"Name": "ARGNS_' + udf + '","Description": "' + udf + '","Type": "db_Alpha", "Size": 100,"EditSize": 100, "TableName": "OITM"}'
            intento = self.insercion('UserFieldsMD', cuerpo)
            if intento == 'e' or intento == 'a':
                udfsExistentes.append(udf)
            elif intento:
                udfsNuevos.append(udf)
            elif not intento:
                udfsConError.append(udf)
        return udfsNuevos, udfsExistentes, udfsConError

    # Paso final para insertar un modelo, simplemente lo insertamos
    def insertar_modelo(self, cuerpo):
        a = self.insercion('ARGNS_MODEL', cuerpo)
        return a

    def eliminarCreados(self, db: BaseDatos, listaCreados: {}):
        for clave in listaCreados:
            if clave == 'productLineCode':
                self.eliminar('ARGNS_PRODLINE', listaCreados[clave])
            elif clave == 'productGroupCode':
                db.eliminar('"' + self.dataBase + '"."@ARGNS_MODELGRP"', 'U_ProdLine', listaCreados[clave])
            elif clave == 'AFsegmentation':
                self.eliminar('ARGNS_APPTEXGRPS',
                              self.consulta('ARGNS_APPTEXGRPS', 'Name', listaCreados[clave], 'Code'))
            elif clave == 'season':
                db.eliminar('"' + self.dataBase + '"."@ARGNS_SEASON"', 'Code', listaCreados[clave])
            elif clave == 'collectionCode':
                self.eliminar('ARGNS_COLLECTION',
                              self.consulta('ARGNS_COLLECTION', 'Name', listaCreados[clave], 'Code'))
            elif clave == 'brand':
                db.eliminar('"' + self.dataBase + '"."@ARGNS_BRAND"', 'Name', listaCreados[clave])
            elif clave == 'division':
                db.eliminar('"' + self.dataBase + '"."@ARGNS_DIV"', 'Name', listaCreados[clave])
            elif clave == 'year':
                db.eliminar('"' + self.dataBase + '"."@ARGNS_YEAR"', 'U_Year', listaCreados[clave])
            elif clave == 'sizeChart':
                self.eliminar('ARGNS_SCALE', self.consulta('ARGNS_SCALE', 'Name', listaCreados[clave], 'Code'))
            elif clave == 'color':
                for color in listaCreados[clave]:
                    self.eliminar('ARGNS_COLOR', color)
            db.accept()

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #                                       --- Funciones SKUs ---
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def insertSku(self, id, descripcion, color, modelo, sizeChart, talla, pais, ano, division, season, codigoBarra,
                  udfs):
        try:
            URL = self.URL + "Items"
            cuerpoTupla = {"ItemCode": str(id), "ItemName": str(descripcion), "U_ARGNS_COL": str(color),
                           "U_ARGNS_MOD": str(modelo), "U_ARGNS_SCL": str(sizeChart), "U_ARGNS_SIZE": str(talla),
                           "U_ARGNS_COO": str(pais), "U_ARGNS_YEAR": str(ano), "U_ARGNS_DIV": str(division),
                           "U_ARGNS_SEASON": str(season), "BarCode": str(codigoBarra)}
            cuerpoTupla.update(udfs)
            cuerpoInsertar = str(cuerpoTupla).replace("'", '"')
            r = requests.post(URL, data=cuerpoInsertar, verify=False, headers=self.headers)
            data = r.json()
            if 'error' in data:
                print(cuerpoInsertar)
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False

    def cambiarEstadoSKU(self, code):
        URL = self.URL + "ARGNS_MODEL('" + str(code) + "')"
        requests.patch(URL, verify=False, headers=self.headers, data='{"U_SkuGen": "Y"}')

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #                                       --- Funciones PREPACKs ---
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def retornarSizeRun(self, sizeRun):
        URL = self.URL + "ARGNS_SIZERUNSCALE?$filter=U_SizeRunCode eq '" + str(sizeRun) + "'"
        peticion = requests.get(URL, verify=False, headers=self.headers)
        return peticion.json()

    def insertar_prepack(self, db: BaseDatos, codigo, descripcion, modelo, segmentacion, color, warehouse,
                         priceList, escala, sizeRun, codigoBarra):

        descripcionColor = self.consulta('ARGNS_COLOR', 'U_ColCode', color, 'U_ColDesc')

        listaTallesCantidades = []
        tallesCantidades = self.obtenerCantidades(sizeRun)
        for talle in tallesCantidades:
            valorTemporal = {
                "Code": db.siguienteCode('"' + self.dataBase + '"."@ARGNS_PREPACK"'),
                "U_ColDesc": descripcionColor,
                "U_ColCode": color,
                "U_SizeCode": talle,
                "U_Value": tallesCantidades[talle],
                "U_SclCode": escala,
                "U_Sruncode": sizeRun
            }
            listaTallesCantidades.append(valorTemporal)


        diccionarioInsertar = {"Code": db.siguienteCode('"' + self.dataBase + '"."@ARGNS_PREPACK"'),
                               "U_PpCode": str(codigo), "U_PpDesc": str(descripcion),
                               "U_ModCode": str(modelo), "U_Comb": 'C', "U_Sruncode": sizeRun,
                               "U_PriceList": priceList, "U_WhsCode": warehouse,
                               "U_SclCode": escala,
                               "U_PpType": "M",
                               "U_AFSeg": self.consulta('ARGNS_APPTEXGRPS', 'Name', segmentacion, 'Code'),
                               'ARGNS_PREPACKLNSCollection': listaTallesCantidades}

        # TODO activar la linea de abajo y desactivar la de 2 abajo
        # self.insercion('ARGNS_PREPACK', str(diccionarioInsertar))
        prepack = diccionarioInsertar
        item = self.insertarItemPrepack(codigo, color, sizeRun, modelo, warehouse, codigoBarra)
        bill = self.insertarBillMaterial(codigo + '-' + color + '-' + sizeRun, tallesCantidades, warehouse, priceList, modelo + '-' + color)

        print(str(json.dumps(prepack)).replace("'", '"'))
        print(str(json.dumps(item)).replace("'", '"'))
        print(str(json.dumps(bill)).replace("'", '"'))

        resultadoPrepack = self.insercion('ARGNS_PREPACK', str(json.dumps(prepack)).replace("'", '"'))
        resultadoItem = self.insercion('Items', str(json.dumps(item)).replace("'", '"'))
        resultadoBill = self.insercion('ProductTrees', str(json.dumps(bill)).replace("'", '"'))

        print(resultadoPrepack)
        print(resultadoItem)
        print(resultadoBill)


        if resultadoPrepack and resultadoItem and resultadoBill:
            return True
        else:
            return False


    def obtenerCantidades(self, sizeRun):
        diccionario = {}
        for a in self.retornarSizeRun(sizeRun)['value'][0]['ARGNS_SZRUNSCALELNCollection']:
            diccionario[a['U_SizeCode']] = str(a['U_Qty'])
        return diccionario

    def insertarItemPrepack(self, codigoPrepack, color, sizeRun, model, warehouse, codigoBarra):
        diccionarioItem = {
            "ItemCode": codigoPrepack + '-' + color + '-' + sizeRun,
            "ItemName": codigoPrepack + '-' + color + '-' + sizeRun,
            "BarCode": codigoBarra,
            "DefaultWarehouse": warehouse,
            "U_ARGNS_MOD": model,
        }

        return diccionarioItem

    def insertarBillMaterial(self, code, listaTallesCantidades, warehouse, priceList, codigoSinSizeRun):
        tabla = []

        for talle in listaTallesCantidades:
            temporal = {"ItemCode": codigoSinSizeRun + '-' + talle,
                    "Quantity": listaTallesCantidades[talle],
                    "PriceList": priceList,
                    "Warehouse": warehouse}
            tabla.append(temporal)

        diccionarioInsertar = {"TreeCode": code, "PriceList": priceList,
            "Warehouse": warehouse,
            "ProductDescription": code, 'ProductTreeLines': tabla}

        return diccionarioInsertar


# print(conexionServicio.connectedStatus())

# Ejemplo para traer un item
# print(conexionServicio.getItem('A2020'))
# print(conexionServicio.getItem('A2020'))
# print(conexionServicio.insertSimple('itemDePrueba', 'itemDePruebaDescripcion'))
# print(conexionServicio.insertSku('276-A0532-1101-6300-39', '276-A0532-1101', '6300', '276-A0532-1101', 'MAN', '39',
#                                 'India', '2020', 'M', '2020W', 'CodiguitoBarras'))

# Ejemplo para insertar un item

if __name__ == '__main__':
    URL = "https://192.168.0.22:50000/b1s/v1/"
    dataBase = "SBODEMOAR3"
    userName = "manager"
    password = "1234"
    direccion = '192.168.0.22'
    puerto = '30015'
    usuario = 'SYSTEM'
    clave = 'Argns1050'

    db = BaseDatos(direccion, puerto, usuario, clave)
    conexionServicio = SapSL(URL, dataBase, userName, password)

    conexionServicio.insertar_prepack(db, '311-10108-2100-6100-601', '601', '311-10108-2100',
                                            'SHOES', '6100', '01', '10', 'MAN',
                                            'FirstSizeRun', '7613146337935')
