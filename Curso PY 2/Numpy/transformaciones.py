import numpy as np

arr_ent = np.random.randint(0,10,(3,4))
print(arr_ent)

arr_ent.astype(float)
print(arr_ent)

arr_ent.sort()
print(arr_ent)

arr_ent.sort(axis = 0)
print(arr_ent)

arr_ent = arr_ent.reshape(6,2)
print(arr_ent)

plano_Arr = arr_ent.flatten()
print(plano_Arr)
print(arr_ent)

lista_arr = plano_Arr.tolist()
print(lista_arr)