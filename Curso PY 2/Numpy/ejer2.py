import numpy as np

a = np.array([[8, 5], [3, 4]], float)
print (a, "\n-------------------------")

## determinante de matriz ( tiene que ser cuadrada 2x2, (8*4)-(5*3) = 32-15 = 17)
print (np.linalg.det(a))
print ("-------------------------")

####

vals, vecs = np.linalg.eig(a)

print (vals, "\n-------------------------")
print (vecs, "\n-------------------------")