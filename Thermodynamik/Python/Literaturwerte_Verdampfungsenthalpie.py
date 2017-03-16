# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:09:23 2017

@author: grldm
"""

import Praktikum as prak
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt
import Rauschmessung as Rm

start_time=timeit.default_timer()

x_C_1 = [0, 25, 40, 60, 80, 100, 120, 140, 160, 180, 200]
y_1 = [45.054, 43.99, 43.35, 42.482, 41.585, 40.657, 39.684, 38.643, 37.518, 36.304, 34.962]

a_1 = [0, 200]
b_1 = [45.054, 34.962]

x_C_2 = [60, 80, 100]
y_2 = [42.482, 41.585, 40.657]

a_2 = [60, 100]
b_2 = [42.482, 40.657]

m = (y_2[2] - y_2[0])/(x_C_2[2] - x_C_2[0])
b = y_2[0] - m * x_C_2[0]

#plotte Literaturwerte als blaue Punkte und fit als rote Linie
fig1, ax1 = plt.subplots()
ax1.set_xlabel("Temperatur [K]")
ax1.set_ylabel("Verdampfungsenthalpie [kJ/mol]")
ax1.set_title("")
plt.plot(a_2, b_2, color='r')
plt.errorbar(x_C_2, y_2, color = 'b', fmt='.')
plt.figtext(0.6,0.7,
            '\n a= '+str(np.round(m,3))+'\n'
            +' b= '+str(np.round(b,3)))
fig1.show()

#Gibt Literaturwert für Lambda in Abhängigkeit von T in Celsius
def Lambda(T):
    x_C_2 = [60, 80, 100]
    y_2 = [42.482, 41.585, 40.657]

    a_2 = [60, 100]
    b_2 = [42.482, 40.657]

    m = (y_2[2] - y_2[0])/(x_C_2[2] - x_C_2[0])
    b = y_2[0] - m * x_C_2[0]
    return np.round((m * T + b), 3)

print(Lambda(50))

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))