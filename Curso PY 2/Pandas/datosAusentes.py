import numpy as np
import pandas as pd

df = pd.DataFrame({
        'VarA:': ['aa', None, 'cc'],
        'VarB:': [20, 30, None],
        'VarC:': [1234, 3456, 6789]
},
    index=['CASO a', 'CASO b', 'CASO c'])

print (df)
#print(pd.isnull(df))
#print(df.dropna(subset=['VarB:', 'VarC:']))
print(df.fillna(""))
print(df.fillna(df.mean()))