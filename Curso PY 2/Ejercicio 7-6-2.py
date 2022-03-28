


class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangulo:
    def __init__(self, inicio = Punto (0,0), fin = Punto (0,0)):
        self.inicio = inicio
        self.fin = fin
        self.base = abs (self.inicio.x - self.fin.x)
        self.altura = abs (self.inicio.y - self.fin.y)
        self.area = self.base * self.altura
    def mostrar_base(self):
        print (f'la base del rectángulo es {self.base}')
    def mostrar_altura(self):
        print (f'la altura del rectángulo es {self.altura}')
    def mostrar_area(self):
        print (f'el área del rectángulo es {self.area}')

a = Punto(1,2)
b = Punto(3,4)

rec = Rectangulo(a,b)
rec.mostrar_base()
rec.mostrar_altura()
rec.mostrar_area()
