import numpy as np
import pandas as pd

data = pd.read_csv('data_celular.csv', 
                    header=0, 
                    index_col=0, 
                    names=['indice', 'fecha', 'item', 'mes', 'red', 'tipo_red'], 
                    parse_dates=['fecha'])

print (data.head())
print ("\n filas que tiene: ")
print (data["item"].count())
#print(data['duracion'][data['item'] == 'call'].sum())
#print (data.groupby('mes').groups.keys())
print (data.groupby('mes').sum())
