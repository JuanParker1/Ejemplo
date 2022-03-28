


class conexion:
    def __init__(self, direccion, puerto, usuario, clave):
        self.conn = dbapi.connect(