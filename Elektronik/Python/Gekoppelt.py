# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 08:36:33 2017

@author: grldm
"""

import Praktikum as prak
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt

start_time=timeit.default_timer()

#Lese Daten ein
M_S_1 = prak.lese_lab_datei('lab/Koppel_mitAbstand_1.lab')
t = M_S_1[:, 1]
U_Mess_1 = M_S_1[:, 2]
U_Mess_2 = M_S_1[:, 3]

#fourier
f_1, U_1 = prak.fourier_fft(t, U_Mess_1)
f_2, U_2 = prak.fourier_fft(t, U_Mess_2)

#finde peaks
peak1_1 = prak.peak(f_1, U_1, 700, 800)
peak1_2 = prak.peak(f_1, U_1, 450, 520)
peak2_1 = prak.peak(f_2, U_2, 700, 800)
peak2_2 = prak.peak(f_2, U_2, 750, 900)

print(peak1_1)
print(peak2_1)

#plotte Frequenzspektrum
x = [peak1_1, peak1_1]
y = [0,1600]
a = [peak1_2, peak1_2]
b = [0,1600]
fig1, ax1 = plt.subplots()
plt.font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 21}
ax1.set_xlabel("Frequenz [Hz]", **plt.font)
ax1.set_ylabel("Spannung [V]", **plt.font)
ax1.set_title("Frequenzspektrum der Spannung", **plt.font)
plt.plot(f_2, U_2)
#plt.plot(x, y)
#plt.plot(a, b)
plt.figtext(0.7,0.57,
            '\n $f_+$= '+str(np.round(peak1_1,3))+' Hz\n'
            +'$f_-$= ' + str(np.round(peak1_2, 3))+' Hz\n', **plt.font)
plt.xlim(500, 900)
fig1.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))