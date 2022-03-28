n_1 = float(input("Ingrese el primer número: \n" ))
n_2 = float(input("Ingrese el segundo número: \n"))

print ('que queres hacer rayy')
print ('[1]. Sumar')
print ('[2]. Restar')
print ('[3]. Multiplicar')

opcion = input("Ingrese una opción: \n")

if opcion == "1":
    print (f'la suma de {n_1} mas {n_2} es: {n_1+n_2}')
elif opcion == "2":
    print (f'la resta de {n_1} menos {n_2} es: ', n_1-n_2)
elif opcion == "3":
    print (f'la multi de {n_1} con {n_2} es: {n_1 * n_2}')
else:
    print ("Opción incorrecta RAAAYYYY")