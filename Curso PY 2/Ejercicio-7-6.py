import math


class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    def cuadrante(self):
        if self.x > 0 and self.y > 0:
            print (f'{self} está en el primer cuadrante')
        elif self.x < 0 and self.y > 0:
            print (f'{self} está en el segundo cuadrante')
        elif self.x < 0 and self.y < 0:
            print(f'{self} está en el tercer cuadrante')
        elif self.x > 0 and self.y < 0:
            print(f'{self} está en el cuarto cuadrante')
        
        elif self.x != 0 and self.y == 0:
            print(f'{self} está en el eje x')
        
        elif self.x == 0 and self.y != 0:
            print(f'{self} está en el eje y')
        else:
           print(f'{self} está en el origen')
    def vector(self, p):
        return (f'el vector qe une los puntos {self} y {p} es igual a {p.x-self.x} y {p.y-self.y}')
    def distancia(self, p):
        mod = math.sqrt ((p.x-self.x)**2 + (p.y-self.y)**2)
        print(f'la distancia entre {self} y {p} es {mod}')
    
a = Punto(1,2)
b = Punto(3,4)
c = Punto(1,2)
c.cuadrante()
a.vector(b)
a.distancia(b)
print(a)