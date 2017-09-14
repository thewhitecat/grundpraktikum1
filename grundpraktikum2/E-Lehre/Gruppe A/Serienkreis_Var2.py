# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:54:41 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data = p.lese_lab_datei('10Ohm.lab')
kleiner = False

I = data[:,3]
phi = data[:,4]
UC = data[:,5]
UL = data[:,6]
f = data[:,8]

x_Achse = np.full(len(phi), 0)
obere = np.full(len(phi), -45)
untere = np.full(len(phi), 45)

sol_zero = AM.Schnittpunkte(f, phi, x_Achse)
sol_obere = AM.Schnittpunkte(f, phi, obere)
sol_untere = AM.Schnittpunkte(f, phi, untere)

#abgelesen
if kleiner == True:
    f_zero = 2088.437
    f_untere = 1742.037
    f_obere = 2549.634
else:
    f_zero = 2110.274
    f_untere = 1516.288
    f_obere = 2975.858

#Unsicherheit beim Ablesen:
sig_f = 5

#Unsicherheit beim Ausrechnen:
sig_f_ber = 20/np.sqrt(12)

f_zero_ber = (f[sol_zero[0]] + f[sol_zero[0]+1])/2
f_obere_ber = (f[sol_obere[0]] + f[sol_obere[0]+1])/2
f_untere_ber = (f[sol_untere[0]] + f[sol_untere[0]+1])/2

Q_ber = f_zero_ber / (f_obere_ber - f_untere_ber)
Q_ab = f_zero / (f_obere - f_untere)

sig_Q_ab = Q_ab * np.sqrt((sig_f/f_zero)**2 + (sig_f/f_obere)**2 + (sig_f/f_untere)**2)
sig_Q_ber = Q_ber * np.sqrt((sig_f_ber/f_zero_ber)**2 + (sig_f_ber/f_obere_ber)**2 + (sig_f_ber/f_untere_ber)**2)

print("Güte aus Schnittpunkten: \n {0:2.4f} +/- {1:2.4f} (berechnet) \n {2:2.4f} +/- {3:2.4f} (abgelesen)".format(round(Q_ber, 4), round(sig_Q_ber, 4), round(Q_ab, 4), round(sig_Q_ab, 4)))

plt.figure(1)
ax1=plt.subplot(111)
plt.plot(f, phi)
plt.axvline(f_zero, color = 'r')
plt.axvline(f_untere, color = 'r')
plt.axvline(f_obere, color = 'r')
plt.axvline(f_obere_ber, color = 'g')
plt.axvline(f_untere_ber, color = 'g')
plt.axvline(f_zero_ber, color = 'g')
plt.axhline(0, color = 'r')
plt.axhline(45, color = 'r')
plt.axhline(-45, color = 'r')
plt.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))