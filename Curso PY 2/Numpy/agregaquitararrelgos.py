import numpy as np

arr = np.arange(0,20,2)
print(arr)

# random matriz de 3x4
arr_flot = np.random.rand (4,3)
print(arr_flot)

# arreglo matriz de 0 a 10 numero y de 2x3
arr_ent = np.random.randint(0,10,(2,3))
print(arr_ent)

# arreglo full con matriz 3x3 con valor 5
arr_full = np.full((3,3),5)
print(arr_full)

#funciones que nos permiten agregar o quitar elementos

npappend = np.append(arr,[12,13,14,15])
print (npappend)

npinsert = np.insert(arr,2, [0,1,2,3])
print (npinsert)

npdelete = np.delete(arr,2, axis = 0)
print (npdelete)