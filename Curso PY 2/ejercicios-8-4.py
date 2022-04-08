class vehiculos():
    def __init__(self, color, ruedas):
        self.color = color
        self.ruedas = ruedas

    def __str__(self) -> str:
        return ("Color {}, {} ruedas".format(self.color, self.ruedas))

class auto (vehiculos):
    def __init__(self, color, ruedas, velocidad, cilindrada):
        self.color = color
        self.ruedas = ruedas
        self.velocidad = velocidad
        self.cilindrada = cilindrada
    def __str__(self) -> str:
        return ("Color {}, {} velocidad, {} ruedas,  {} cilindrada".format(self.color,  self.velocidad,self.ruedas, self.cilindrada))

class camioneta (auto):
    def __init__(self, color, ruedas, velocidad, cilindrada, carga):
        super().__init__(color, ruedas, velocidad, cilindrada)
        self.carga = carga


    def __str__(self) -> str:
        return (super().__str__() + ", {} carga".format(self.carga))

class bicicleta (vehiculos):
    def __init__(self, color, ruedas, tipo):
        super().__init__(color, ruedas)
        self.tipo = tipo

    def __str__(self) -> str:
        return (super().__str__() + ",  tipo {}".format(self.tipo))

class moto (bicicleta):
    def __init__(self, color, ruedas, tipo, velocidad, cilindraje):
        super().__init__(color, ruedas, tipo)
        self.velocidad = velocidad
        self.cilindraje = cilindraje

    def __str__(self) -> str:
        return (super().__str__() + ", {} velocidad, {} cilindraje".format(self.velocidad, self.cilindraje))

def catalogar (vehiculos, ruedas = None):
    if ruedas != None:
        contador = 0
        for v in vehiculos:
            if v.ruedas == ruedas:
                contador += 1
        print("\nSe han encontrado {} vehículos con {} ruedas:".format(contador, ruedas))
    for v in vehiculos:
        if ruedas == None:
            print (type(v).__name__, v)
        else:
            if v.ruedas == ruedas:
                print (type(v).__name__, v)


vehiculos = [
    auto("Azul", 4, 150, 1200),
    camioneta("Blanco", 4, 100, 1300, 1500),
    bicicleta("Verde", 2, "urbana"),
    moto("Negro", 2, "deportiva", 180, 900)
]

# ford = auto("rojo", 4, 200, "1.8")
# print(ford)

catalogar (vehiculos, 2)
