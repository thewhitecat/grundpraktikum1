# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:36:03 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data = p.lese_lab_datei('5Ohm.lab')
kleiner = False

U = data[:,2]
I = data[:,3]
phi = data[:,4]
UC = data[:,5]
UL = data[:,6]
f = data[:,8]

#abgelesen
if kleiner == True:
    f_schnitt = 2101.633
    UL_schnitt = 3.696443
    U_f_schnitt = 1.41231
else:
    f_schnitt = 2102.349
    UL_schnitt = 2.086694
    U_f_schnitt = 1.41231

#Unsicherheit beim Ablesen der Spannung
sig_U_ab = 0.0014

#Unsicherheit beim Messen der Spannung
sig_U = 0.0014

schnitt = AM.Schnittpunkte(f, UC, UL)

f_schnitt_ber = (f[schnitt[0]] + f[schnitt[0] + 1])/2

Q_ber = (UL[schnitt[0]] + UL[schnitt[0] + 1])/2 / ((U[schnitt[0]] + U[schnitt[0]])/2)
Q_ab = UL_schnitt / U_f_schnitt

sig_Q_ab = Q_ab * np.sqrt((sig_U_ab / UL_schnitt)**2 + (sig_U_ab / U_f_schnitt)**2)
sig_Q_ber = Q_ber * np.sqrt((sig_U / ((UL[schnitt[0]] + UL[schnitt[0] + 1])/2))**2 + (sig_U / ((U[schnitt[0]] + U[schnitt[0]])/2))**2)

print("Güte aus Schnittpunkten: \n {0:2.4f} +/- {1:2.4f} (berechnet) \n {2:2.4f} +/- {3:2.4f} (abgelesen)".format(round(Q_ber, 4), round(sig_Q_ber, 4), round(Q_ab, 3), round(sig_Q_ab, 3)))

plt.figure(1)
ax1=plt.subplot(111)
plt.plot(f, UL)
plt.plot(f, UC)
plt.plot(f, U)
ax1.set_ylabel("Spannung [V]")
ax1.set_xlabel("Frequenz [Hz]")
ax1.set_title("Spannungsverlauf")
plt.axvline(f_schnitt, color = 'r')
plt.axhline(UL_schnitt, color = 'r')
plt.axvline(f_schnitt_ber, color = 'g')
plt.show()

#Variante 4: Berechnen aus Größen der Bauteile
#mit der Brücke gemessen:
L = 1.275e-3
C = 4.598e-6
if kleiner == True:
    R = 5.182
else:
    R = 10.035

sig_R = 1e-3
sig_C = 1e-9
sig_L = 1e-6

Q = 1./R * np.sqrt(L/C)
sig_Q = Q * np.sqrt((sig_R / R)**2 + (sig_C / (2*C))**2 + (sig_L / (2*L))**2)

print("Güte aus Größen der Bauteile: \n {0:2.4f} +/- {1:2.4f}".format(round(Q, 4), round(sig_Q, 4)))

#mitteln der Werte für die Güte:
#5Ohm Widerstand:
guten_k = [2.6392, 2.5860, 2.6170, 2.6667, 2.6125, 2.6282]
sig_guten_k = [0.0245, 0.0235, 0.003, 0.0289, 0.0276, 0.0028]
gute_k = AM.gew_mittelwert(np.array(guten_k), np.array(sig_guten_k))

#10Ohm Widerstand:
guten_g = [1.5003, 1.4458, 1.4780, 1.4857, 1.4452, 1.4847]
sig_guten_g = [0.0085, 0.0078, 0.002, 0.0096, 0.009, 0.0018]
gute_g = AM.gew_mittelwert(np.array(guten_g), np.array(sig_guten_g))

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))