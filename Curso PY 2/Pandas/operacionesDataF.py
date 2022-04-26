import pandas as pd
import numpy as np

d = [np.random.randint (50, size=(10))]
print(d)
'''
Comunes
'''
df = pd.DataFrame(d)
'''
TANSPUESTA
'''
#df = pd.DataFrame(d).T

df['Nueva Columna'] = 10
df['Experiencias'] = 5
#df['Perdidas'] = [(i+2)*np.e for i in df['Nueva Columna']]
df['Nueva Columna'] = df['Experiencias']*100
df.columns = ['a1','a2','a3','aa4','a5','aa6','a7','aa8','a9','A10','Nueva Columna', 'Experiencias']
# modificar una columa
df['a1'] = df['a1']/2
# eliminar una columna
#del df['a1']
# eliminar una fila
#df.drop(0, axis=0)
# eliminar una fila y una columna
#df.drop(0, axis=0).drop('a1', axis=1)
#suma de toda la columna
#df['a1'].sum()
#suma de toda la fila
#df.sum(axis=1)
#suma de toda la fila y columna
#df.sum()
#resta de toda la columna
#df['a1'].mean()
#resta de toda la fila
#df.mean(axis=1)
#resta de toda la fila y columna
#df.mean()
#valor maximo de la columna
#df['a1'].max()
#valor maximo de la fila
#df.max(axis=1)
#valor maximo de la fila y columna
#df.max()
#valor minimo de la columna
#df['a1'].min()
#valor minimo de la fila
#df.min(axis=1)
#valor minimo de la fila y columna
#df.min()
print (df)
print(df.columns)
