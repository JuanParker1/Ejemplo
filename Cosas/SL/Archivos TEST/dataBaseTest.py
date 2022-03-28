from dataBase import BaseDatos


def test():
    # Direccion de la Base de Datos
    direccion = '192.168.0.22'
    puerto = '30015'
    usuario = 'SYSTEM'
    clave = 'Argns1050'
    db = BaseDatos(direccion, puerto, usuario, clave)

    db.siguienteCode('"SBODEMOAR2"."@ARGNS_MODEL"')


def limpiarBase():
    # Direccion de la Base de Datos
    direccion = '192.168.0.22'
    puerto = '30015'
    usuario = 'SYSTEM'
    clave = 'Argns1050'
    db = BaseDatos(direccion, puerto, usuario, clave)

    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_PRODLINE" WHERE "DocEntry">6')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_MODELGRP" WHERE "Code"<>' + "'01' AND " + '"Code"<>' + "'02'")
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_DIV" WHERE "Code"<>' + "'RA' AND " + '"Code"<>' + "'PT'")
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_PRODLINE" WHERE "DocEntry">4')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_SEASON" WHERE "Code" NOT IN '
                '(SELECT TOP 6 "Code" FROM "SBODEMOAR2"."@ARGNS_SEASON")')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_COLLECTION"')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_BRAND" WHERE "Code" NOT IN '
        '(SELECT TOP 3 "Code" FROM "SBODEMOAR2"."@ARGNS_BRAND")')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_YEAR" WHERE "Code" NOT IN '
        '(SELECT TOP 2 "Code" FROM "SBODEMOAR2"."@ARGNS_YEAR")')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_MODEL_COLOR"')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_APPTEXGRPS" WHERE "Code" NOT IN '
        '(SELECT TOP 4 "Code" FROM "SBODEMOAR2"."@ARGNS_APPTEXGRPS")')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_MODVENDOR" WHERE "Code" NOT IN '
        '(SELECT TOP 3 "Code" FROM "SBODEMOAR2"."@ARGNS_MODVENDOR")')
    db.ejecutar(
        'DELETE FROM "SBODEMOAR2"."@ARGNS_MODEL_SIZE"')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_MODEL" WHERE "DocEntry">12')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."@ARGNS_COLOR"')
    db.ejecutar('DELETE FROM "SBODEMOAR2"."OITM" WHERE LOWER("ItemCode") LIKE' + " LOWER('%test%')")
    db.accept()

limpiarBase()
#test()
