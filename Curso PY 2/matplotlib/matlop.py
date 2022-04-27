import numpy as np
import matplotlib.pyplot as plt

#fig, panel = plt.subplots()

#x = np.linspace(0, 4*np.pi, 100)
#y = np.sin(x)

#panel.plot(x, y)

#fig, (panel1, panel2) = plt.subplots(2,1)

#figura 1
# x1 = np.linspace(0, 4*np.pi, 100)
# y1 = np.sin(x1)
# panel1.plot(x1, y1, 'tab:green')

#figura 2
# x2 = np.linspace(0, 4*np.pi, 100)
# y2 = np.cos(x2)
# panel2.plot(x2, y2)

#guardar la figura
#plt.savefig('figura_sin_cos.png')

fig, pan_1 = plt.subplots(1,1)

pan_2 = pan_1.twinx()

x1 = np.linspace(0, 4*np.pi, 100)
y1 = np.sin(x1)

pan_1.plot(x1, y1, 'y')

x2 = np.linspace(0, 4*np.pi, 100)
y2 = np.cos(x2)

pan_2.plot(x2, y2, 'r')

plt.savefig('figura_sin_cos_trans.png')