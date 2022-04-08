import numpy as np

# a = np.array([1, 2, 3, 4, 5], float)
# b = np.array([6, 7, 8, 9, 10], float)
# print (np.dot(a, b))
# print (a.dot(b)) ## producto escalar para array bidimensional

#a = np.array([[1, 3], [4, 5]], float)
#b = np.array([[6, 8], [9, 10]], float)

#print (a, "\n-------------------------")
#print (b, "\n-------------------------")

## producto matricial (No es el recomendado)
#print (np.dot(a, b))

## Operador add
#print (a @ b)

################################################################

## matriz de distintos ordenes

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], float)
b = np.array([[4, 5, 6]], float)

print (b, "\n-------------------------")
print (a, "\n-------------------------")

## producto matricial (No es el recomendado) el orden de los factores si altera el producto
print (np.dot(b, a))


## Operador add
print (b @ a)

## Producto matricial de array bidimensional
print (np.matmul(b,a))