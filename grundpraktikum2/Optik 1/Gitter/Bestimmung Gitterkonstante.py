# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 15:06:29 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data_raw = np.genfromtxt('Gitterkonstante.txt', delimiter = ',', skip_header = 2);

winkel_1 = np.transpose(np.array([data_raw[:,2], data_raw[:,3]]))
data_1 = AM.degtorad(winkel_1)
winkel_2 = np.transpose(np.array([data_raw[:,4], data_raw[:,5]]))
data_2 = AM.degtorad(winkel_2)
winkel = (np.array(data_1) + np.array(data_2))/2

#Aus Raschmessung
Winkel_Fehler = 2 * 0.00029807171525957543 / np.sqrt(2)
Winkel_Nullte_Ordnung = 1.4755304384568726
def linreg(phi):
    X = data_raw[:,0] * data_raw[:,1]
    Y = np.sin(phi) + np.sin(Winkel_Nullte_Ordnung - winkel - phi)
    EY = Winkel_Fehler * np.cos(Winkel_Nullte_Ordnung - winkel - phi)

    sol = p.lineare_regression(X, Y, EY)
    return sol[4]/13

bogenminute = 0.0002908882086657216
tries = np.arange(-2000 * bogenminute, 2000 * bogenminute, bogenminute / 10)
chiqperdof = []
for i in range(len(tries)):
    chiqperdof += [linreg(tries[i])]   

min, j = AM.minausarray(chiqperdof)

X = data_raw[:,0] * data_raw[:,1]
Y = np.sin(tries[j]) + np.sin(Winkel_Nullte_Ordnung - winkel - tries[j])
EY = Winkel_Fehler * np.cos(Winkel_Nullte_Ordnung - winkel - tries[j])
sol = p.lineare_regression(X, Y, EY)

d = 1/sol[0]
sig_d = d * sol[1] / sol[0]

print("d = (", np.abs(d), " +/- ", sig_d, ") nm")

#plotte schön
plt.figure(1)
ax1=plt.subplot(211)
ax1.set_ylabel("sin(theta) [1]")
x = np.array([X[6], X[13]])
y = sol[0] * x + sol[2]
ax1.set_ylabel("sin(theta) [1]")
ax1.set_title("")
plt.figtext(0.75,0.7,
            '\n a= ('+str(np.round(sol[0],6))+' +/- '+str(np.round(sol[1],8))+') 1/nm \n'
            +' b= ('+str(np.round(sol[2],6))+' +/- '+str(np.round(sol[3],6))+')  \n'
            +'$\chi ^2 / ndof$= ' + str(np.round(sol[4]/13, 3))+'  \n'
            +' $\phi $ = '+str(np.round(tries[j],6))+' rad')
plt.plot(x, y, color='r')
plt.errorbar(X, Y, yerr=EY, fmt='.', color='b')

ax2=plt.subplot(212,sharex=ax1)
x_r = np.array([-1000, 1000])
y_r = np.array([0, 0])
H = np.full(Y.size, 1)
H_err = np.full(Y.size, 1)
for i in range(Y.size):
    H[i] = Y[i] - sol[0] * X[i] - sol[1]
    H_err[i] = np.sqrt(EY[i]**2)
ax2.set_xlabel("$n \cdot \lambda$ [nm]")
ax2.set_ylabel("Residuen [1]")
plt.plot(x_r, y_r, color='r')
plt.errorbar(X, H, yerr=H_err, fmt='.', color='b')
plt.show()

'''
#plotte ersten Fit, ohne Verdrehwinkel
phi_1 = 0
X_1 = data_raw[:,0] * data_raw[:,1]
Y_1 = np.sin(phi_1) + np.sin(Winkel_Nullte_Ordnung - winkel - phi_1)
EY_1 = Winkel_Fehler * np.cos(Winkel_Nullte_Ordnung - winkel - phi_1)
sol_1 = p.lineare_regression(X_1, Y_1, EY_1)
plt.figure(2)
ax1=plt.subplot(211)
ax1.set_ylabel("sin(theta) [1]")
x = np.array([X_1[6], X_1[13]])
y = sol_1[0] * x + sol_1[2]
ax1.set_ylabel("sin(theta) [1]")
ax1.set_title("")
plt.figtext(0.75,0.7,
            '\n a= ('+str(np.round(sol_1[0],6))+' +/- '+str(np.round(sol_1[1],8))+') 1/nm \n'
            +' b= ('+str(np.round(sol_1[2],6))+' +/- '+str(np.round(sol_1[3],6))+')  \n'
            +'$\chi ^2 / ndof$= ' + str(np.round(sol_1[4]/13, 3)))
plt.plot(x, y, color='r')
plt.errorbar(X_1, Y_1, yerr=EY_1, fmt='.', color='b')

ax2=plt.subplot(212,sharex=ax1)
x_r = np.array([-1000, 1000])
y_r = np.array([0, 0])
H = np.full(Y_1.size, 1)
H_err = np.full(Y_1.size, 1)
for i in range(Y_1.size):
    H[i] = Y_1[i] - sol_1[0] * X_1[i] - sol_1[1]
    H_err[i] = np.sqrt(EY_1[i]**2)
ax2.set_xlabel("$n \cdot \lambda$ [nm]")
ax2.set_ylabel("Residuen [1]")
plt.plot(x_r, y_r, color='r')
plt.errorbar(X_1, H, yerr=H_err, fmt='.', color='b')
plt.show()
'''

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))