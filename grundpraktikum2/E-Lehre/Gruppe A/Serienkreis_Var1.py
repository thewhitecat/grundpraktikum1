# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:38:40 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data = p.lese_lab_datei('5Ohm.lab')
kleiner = True

I = data[:,3]
UC = data[:,5]
UL = data[:,6]
f = data[:,8]

sol = AM.getmax(f, I)

#abgelesen
if kleiner == True:
    ab_right = 2513.051
    ab_left = 1724.925
else:
    ab_right = 2882.037
    ab_left = 1495.616

#Unsicherheit beim Ablesen:
sig_f = 5

#Unsicherheit beim Ausrechnen:
sig_f_ber = 20/np.sqrt(12)

Y_const = np.full(len(f), sol[1]/np.sqrt(2))
schnitt = AM.Schnittpunkte(f, Y_const, np.array(I))

f_right = (f[schnitt[1]] + f[schnitt[1]+1])/2
f_left = (f[schnitt[0]] + f[schnitt[0]+1])/2
Q_ber = sol[0] / (f_right - f_left)
Q_ab = sol[0] / (ab_right - ab_left)

sig_Q_ab = Q_ab * np.sqrt((sig_f/sol[0])**2 + 2 * (sig_f/(ab_right - ab_left))**2)
sig_Q_ber = Q_ber * np.sqrt((sig_f_ber/sol[0])**2 + 2 * (sig_f_ber/(f_right - f_left))**2)

print("Güte aus Schnittpunkten: \n {0:2.4f} +/- {1:2.4f} (berechnet) \n {2:2.4f} +/- {3:2.4f} (abgelesen)".format(round(Q_ber, 4), round(sig_Q_ber, 4), round(Q_ab, 4), round(sig_Q_ab, 4)))

plt.figure(1)
ax1=plt.subplot(111)
plt.plot(f, I)
ax1.set_ylabel("Strom [A]")
ax1.set_xlabel("Frequenz [Hz]")
ax1.set_title("Resonanzkurve")
plt.axvline(ab_right, color = 'r')
plt.axvline(ab_left, color = 'r')
plt.axvline(sol[0], color = 'g')
plt.axvline(f_right, color = 'g')
plt.axvline(f_left, color = 'g')
plt.axhline(sol[1]/np.sqrt(2), color = 'r')
plt.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))