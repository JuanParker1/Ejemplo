import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(low=0,high=10, size=(10,2)),
                index=['a','b','c','d','e','f','g','h','i','j'],
                columns = ['COD_EMPLEADO','CLASIFICACION']
)
#print (df.['COD_EMPLEADO'])
#print (df.loc['a'])
#print (df.loc['a':'c'])

#En index se especifica las posiciones de los elementos
print (df.loc[df.index[3:7],'COD_EMPLEADO'])
print (df.iloc[3:7])
print (df.iloc[3:])
#print(df)