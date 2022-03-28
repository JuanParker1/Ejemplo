lista1 = ['avila', 'cafe', 'este', 'narracion', 'buda', 'extra', 'salida']
lista2 = []
suma = 0

for item in lista1:
    if (len(item) >= 2 and (item[0] == item[-1])):
        suma += 1
        lista2.append(item)
print (suma, lista2)
