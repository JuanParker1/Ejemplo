from hdbcli import dbapi


class BaseDatos:
    def __init__(self, direccion, puerto, usuario, clave):
        self.conn = dbapi.connect(
            address=direccion,
            port=puerto,
            user=usuario,
            password=clave,
            sslValidateCertificate=True,
            autocommit=False
        )
        self.cursor = self.conn.cursor()

    def ejecutar(self, instruccion):
        try:
            self.cursor.execute(instruccion)
            return True
        except Exception as e:
            print('Error: ', e)
            print('Instruction: ' + instruccion)
            return False

    def consultar(self, instruccion):
        try:
            retornar = ""
            self.cursor.execute(instruccion)
            rows = self.cursor.fetchall()
            for row in rows:
                for col in row:
                    retornar += ("%s" % col) + " "
                retornar += " "
            return retornar
        except Exception as e:
            print('Error: ', e)
            print('Instruction: ' + instruccion)
            return False

    def consultarArreglo(self, instruccion):
        try:
            retornar = []
            self.cursor.execute(instruccion)
            rows = self.cursor.fetchall()
            for row in rows:
                for col in row:
                    retornar.append("%s" % col)
                retornar += " "
            return retornar
        except Exception as e:
            print('Error: ', e)
            print('Instruction: ' + instruccion)
            return False

    def consultarFilas(self, instruccion):
        try:
            retornar = []
            self.cursor.execute(instruccion)
            rows = self.cursor.fetchall()
            for row in rows:
                actualRow = []
                for col in row:
                    actualRow.append("%s" % col)
                retornar.append(actualRow)
            return retornar
        except Exception as e:
            print('Error: ', e)
            print('Instruction: ' + instruccion)
            return False

    def revert(self):
        self.conn.rollback()

    def accept(self):
        self.conn.commit()

    # Le decimos que elemento queremos obtener y su identificacion, y nos dice si existe (True) o no (False)
    def existe(self, tabla, columna, atributo):
        respuesta = self.consultar('SELECT 1 FROM ' + tabla + ' WHERE "' + columna + '" = ' + "'" + atributo + "'")
        if '1' in respuesta:
            return True
        else:
            return False

    # Le damos el nombre de la tabla, y una clave primaria junto con su valor, para que nos devuelva otro valor de ese
    # mismo objeto todo
    def consultaElemento(self, tabla, columnaEntrada, atributo, columnaSalida):
        respuesta = self.consultar('SELECT "' + columnaSalida + '" FROM ' + tabla + ' WHERE "' + columnaEntrada + '" = ' + "'" + atributo + "'")
        return respuesta
        # if 'error' in data or ('value' in data and not data['value']):
        #     return False
        # else:
        #     return data['value'][0][atributoRetornarNombre]

    def siguienteCode(self, tabla):
        try:
            #respuesta = self.consultar('SELECT MAX(CAST("Code" AS int)) from ' + tabla + ' where isnumeric("Code") = 1')
            respuesta = self.consultar('SELECT MAX(CAST("Code" AS int)) from "ASTOR_MULLER_GERMANY"."@ARGNS_MODEL" where "ASTOR_MULLER_GERMANY".isnumeric("Code") = 1')
            return str(int(respuesta) + 1)
        except Exception:
            return '1'

    def siguienteCodeNew(self, db, tabla):
            try:
                respuesta = self.consultar(
                    'SELECT MAX(CAST("Code" AS int)) from "' + db + '"."' + tabla + '" where "' + db + '".isnumeric("Code") = 1')
                return str(int(respuesta) + 1)
            except Exception:
                return '1'

    def eliminar(self, tabla, columna, valor):
        query = 'DELETE FROM ' + tabla + ' WHERE "' + columna + '" = ' + "'" + valor + "'"
        self.ejecutar(query)


if __name__ == "__main__":
    # Direccion de la Base de Datos
    direccion = '192.168.0.22'
    puerto = '30015'
    usuario = 'SYSTEM'
    clave = 'Argns1050'

    # Generamos la conexion con la base de datos
    db = BaseDatos(direccion, puerto, usuario, clave)


