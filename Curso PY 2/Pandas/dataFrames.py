import numpy as np
import pandas as pd

data = { 'Pais': ['España', 'Francia', 'Italia', 'Alemania', 'Inglaterra', 'Portugal', 'España', 'Francia', 'Italia', 'Alemania', 'Inglaterra', 'Portugal'],
        'Poblacion': [8.5, 66.5, 60.6, 55.4, 52.5, 50.3, 8.5, 66.5, 60.6, 55.4, 52.5, 50.3],
        'Infectados Covid': [80000, 50000, 5000, 8000, 440, 99870, 5730, 3650, 45750, 45760, 456540, 4560]
        }

df = pd.DataFrame(data)
print(df)

#print(df.columns)
#print(df['Poblacion'])
print(df.Poblacion)
print(df.dtypes)