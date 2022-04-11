import numpy as np

# a = np.array(range (64)).reshape((8, 8))
# #print (a)

# a[1,1] = 100
# #print (a)

# a = [0:7:2,0]
# print (a)

data = np.arange(8)
print (data)

print (data < 4)
print (data[data < 4])

amigos = np.array(['Juan', 'Pedro', 'Ana', 'Maria', 'Juan carlos', 'Pedro', 'Ana', 'Maria'])
print ('Juan' in amigos)
print ([amigos != 'Pedro'])