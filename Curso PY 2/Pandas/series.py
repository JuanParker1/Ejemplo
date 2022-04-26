import numpy as np
import pandas as pd


# series = pd.Series([1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988,])
# print(series)

# print (series.values.sum())

# print (series.index)


# series = pd.Series([1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988,], 
#                         index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])


# print(series)
# print(series.index)

# series = pd.Series(np.random.rand(10))
# print(series)

dicci = {'cuadrado de {}'.format(i): i*i for i in range(11)}
#print (dicci)

serie_dic = pd.Series(dicci)
print(serie_dic)