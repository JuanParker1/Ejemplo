import pandas as pd
import numpy as np

clima_p = pd.read_csv('ny_precipitaciones.csv')
#print (clima_p.head())

clima_t = pd.read_csv('ny_temperaturas.csv')
#print (clima_t.shape())

# Filtrtamos los datos de clima
prep_itaca = clima_p[clima_p['NAME'] == 'ITHACA CORNELL UNIVERSITY, NY US']
# print (prep_itaca.shape)

## merge con inner join
itaca_inner_merge = pd.merge(prep_itaca, clima_t)
print(itaca_inner_merge.head())

#Outer join

itaca_outer_merge = pd.merge(prep_itaca, clima_t, how="outer", on=["STATION", "DATE"])
itaca_outer_merge.columns

