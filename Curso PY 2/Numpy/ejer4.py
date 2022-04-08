import numpy as np

arr = np.array([[5,36, 17, 18, 9]])
arr_2 = np.array([[8,24,17,19,9]])

## suma de los elementos de una matriz
print(np.add(arr, arr_2))

## resta de los elementos de una matriz
print(np.subtract(arr, arr_2))

## multiplicacion de los elementos de una matriz
print(np.multiply(arr, arr_2))

##division de los elementos de una matriz
print(np.divide(arr, arr_2))

## boolean si son iguales
print(np.array_equal(arr, arr_2))

## array conformados por los valores minimos y max
print(np.fmin(arr, arr_2))
print(np.fmax(arr, arr_2))
