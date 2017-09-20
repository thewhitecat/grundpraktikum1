# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:48:45 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

#Aus Kalibration###################
Kel = 273.15
k = 1.0350629036742027
off = -286.25043727757156
def temp(T_gem):
    T_real = k * T_gem + off + Kel
    return T_real
###################################

T_raum = 25

T_gem = []
sig_T_gem = []
U = []
sig_U = []

for i in range(0, 10):
    data_bla = p.lese_lab_datei("schwarz/{}.lab".format(50 + 5 * i))
    U += [np.mean(data_bla[:,2])]
    sig_U += [np.std(data_bla[:,2])]
    T_gem += [Kel + np.mean(data_bla[:,3])]
    sig_T_gem += [np.std(data_bla[:,3])]

T = temp(np.array(T_gem))
sig_T = np.sqrt((k * np.array(sig_T_gem))**2)
T4 = T**4 - (Kel + T_raum)**4
sig_T4 = 4 * T**3 * sig_T

sol = p.lineare_regression_xy(np.array(T4), np.array(U), np.array(sig_T4), np.array(sig_U))

#plotte schön
plt.figure(1)
ax1=plt.subplot(211)
x = np.array([2.5 * 10**9, 1.1 * 10**(10)])
y = sol[0] * x + sol[2]
ax1.set_ylabel("Spannung [V]")
ax1.set_title("")
plt.figtext(0.2,0.7,
            '\n a= ('+str(np.round(sol[0],10))+' +/- '+str(np.round(sol[1],10))+') $V/K^4$ \n'
            +' b= ('+str(np.round(sol[2],10))+' +/- '+str(np.round(sol[3],10))+')  V \n'
            +'$\chi ^2 / ndof$= ' + str(np.round(sol[4]/(len(T4) - 2), 3)))
plt.plot(x, y, color='r')
plt.errorbar(T4, U, yerr=sig_U, xerr = sig_T4, fmt='.', color='b')

ax2=plt.subplot(212,sharex=ax1)
x_r = np.array([2.5 * 10**9, 1.1 * 10**(10)])
y_r = np.array([0, 0])
H = np.full(len(U), 1)
H_err = np.full(len(U), 1)
for i in range(len(U)):
    H[i] = U[i] - sol[0] * T4[i] - sol[2]
    H_err[i] = np.sqrt(np.array(sig_U[i])**2 + (sol[0] * np.array(sig_T4[i]))**2)
ax2.set_xlabel("$T^4 - T_0^4$ [$K^4$]")
ax2.set_ylabel("Residuen [V]")
plt.plot(x_r, y_r, color='r')
plt.errorbar(T4, H, yerr=H_err, fmt='.', color='b')
plt.show()

#emissionskoefiizienten
#Konstanten aus Skript
r = 0.108
A_e = np.pi * (0.023/2)**2
A_s = np.pi * (0.035/2)**2
c = 0.276
v = 10**4
sigma = 5.670373 * 10**(-8)

#Steigungen aus den linearen Fits
#Reihenfolge im array: Spiegel, Messing, weis, schwarz
a = [8.2358949959293604e-11, 2.0948303881110427e-10, 1.3981220309235129e-09, 1.351734202543941e-09]
sig_a = [6.3981992350775482e-12, 2.8618193079739291e-11, 8.0701312571509901e-12, 4.6880481305312503e-11]
eps = np.pi * r**2 * c / (A_s * A_e * sigma * v) * np.array(a)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))