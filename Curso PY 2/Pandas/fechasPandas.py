import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

# fecha = pd.to_datetime('24th of December 2015')
# print(fecha)
# print(type(fecha))
# print(fecha.year, fecha.month, fecha.day)

# fecha = datetime.datetime.now()
# print('La fecha de hoy es', fecha)
# print ('Y la fecha en 4 dias sera: ', fecha + pd.to_timedelta(4,unit='D'))

fechas_inicio = pd.date_range(start= '24/4/2020', end= '24/5/2020', freq='D')
print(fechas_inicio)

fechas_fin = pd.date_range(start= '24/5/2020', end='24/6/2020', freq='D')
print(fechas_fin)

lista_equis = []
for i in range (10):
    lista_equis.append(np.random.randint(3,10))

#dataframe
df = pd.DataFrame()
df['fechas_inicioCampaña'] = fechas_inicio [::15]
df['fechas_finCampaña'] = fechas_fin [::15]
#df['lista Target'] = lista_equis
df['dia de inicio'] = df['fechas_inicioCampaña'].dt.day
df['mes de inicio'] = df['fechas_inicioCampaña'].dt.month
df['año de inicio'] = df['fechas_inicioCampaña'].dt.year
df['dia de fin'] = df['fechas_finCampaña'].dt.day
df['mes de fin'] = df['fechas_finCampaña'].dt.month
df['año de fin'] = df['fechas_finCampaña'].dt.year
df['semana de inicio'] = df['fechas_inicioCampaña'].dt.week
df['semana de fin'] = df['fechas_finCampaña'].dt.week

print(df)