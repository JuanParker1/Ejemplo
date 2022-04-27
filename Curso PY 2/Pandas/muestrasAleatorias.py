import numpy as np
import pandas as pd


def crearDataSet(Num=1):
    output = []

    for i in range(Num):
        #crear un rango de fechas semanal (de lunes a lunes)
        fecha = pd.date_range(start='2020-01-01', end='2020-01-07', freq='W-MON')

        #crear valores aleatorios
        data = np.random.randint(low = 25, high = 1000, size = len(fecha))

        #status posibles
        status = ['1', '2', '3']

        #lista de status aleatorios
        status_list = [status[np.random.randint(low = 0, high = len(status))] for i in range(len(fecha))]

        #locales posibles
        states = ['Aguascalientes', 'Baja California', 'Baja California Sur']

        # lista aleatoria de locales
        states_list = [states[np.random.randint(low = 0, high = len(states))] for i in range(len(fecha))]

        output.extend(zip(fecha, data, status_list, states_list))

    return output

dataset = crearDataSet(Num=4)
df = pd.DataFrame(data = dataset, columns = ['fecha', 'data', 'status', 'states'])
print(df)