# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:36:39 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt
import auswertung_01 as aus
import auswertung_nur_Methoden as ausM

start_time=timeit.default_timer()

def Steiner(j, feder=2):
    t0 = []
    t1 = []
    for i in range(5):
        data = p.lese_lab_datei("lab/Feder{:1d}/Steiner/{:1d}verschoben0{:1d}.lab".format(feder, j+1, i+1))
        t = data[:,1]
        U = data[:,2]
        
        indizes = aus.get_peaks(t[:t.size*3/4], U[:U.size*3/4])
        indizes = indizes[:14]
        #print indizes.size
        
        t0.append(t[indizes[0]])
        t1.append(t[indizes[-1]])
        
    t0 = np.array(t0)
    t1 = np.array(t1)
    
    sig_t0 = np.std(t0, ddof=1)/np.sqrt(t0.size) 
    sig_t1 = np.std(t1, ddof=1)/np.sqrt(t1.size)
    
    t0 = np.mean(t0)
    t1 = np.mean(t1)
    
    T = 2*(t1-t0)/(indizes.size-1)
    sig_T = 2*(sig_t0+sig_t1)/(indizes.size-1)
    
    return T, sig_T

#Periodendauern für alle Verschiebungen
T = []
sig_T = []
for i in range(5):
    T_temp, sig_T_temp = Steiner(i)
    T.append(T_temp)
    sig_T.append(sig_T_temp)
T = np.array(T)
sig_T = np.array(sig_T)
T2 = T**2
sig_T2 = 2 * T * sig_T

#Verschiebungen
a = [0.05, 0.1, 0.15, 0.2, 0.25]
sig_a = []
for i in range(5):
    sig_a.append(np.sqrt(i+1) * 0.005/np.sqrt(12))
a = np.array(a)
sig_a = np.array(sig_a)
a2 = a**2
sig_a2 = 2 * a * sig_a

#lin reg
m, em, b, eb, chiq, cov = p.lineare_regression_xy(a2, T2, sig_a2, sig_T2)

#systematische Fehler auf m und b durch verschiebemethode
sys_a = []
for i in range(5):
    sys_a.append((i+1) * 0.0007)
sys_a = np.array(sys_a)
sys_T = 0
systx = 2 * a * sys_a
systy = 2 * T * sys_T
sys_err_m, sys_err_b = ausM.verschiebemethode(a2, T2, sig_a2, sig_T2, systx, systy, m, b)

#berechne J0 und masse des Stabes aus lin reg
D = 0.02971
sig_D = 6.8e-5
J0 = b * D/(4 * np.pi**2)
M_stab = m * D/(4 * np.pi**2)
sig_J0 = np.sqrt((eb * D/(4 * np.pi**2))**2 + (sig_D * b/(4 * np.pi**2))**2)
sig_M_stab = np.sqrt((em * D/(4 * np.pi**2))**2 + (sig_D * m/(4 * np.pi**2))**2)

print("Masse des Stabes: (", M_stab, " +/- ", sig_M_stab, ")kg")
print("Traegheitsmoment des Stabes um Schwerpunktachse J0: (", J0, " +/- ", sig_J0, ")kg*m^2")

#plotte lin reg
x = [a2[0], a2[-1]]
x = np.array(x)
y = m * x + b
fig1, ax1 = plt.subplots()
plt.font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 21}
ax1.set_xlabel("Abstandsquadrat [m^2]", **plt.font)
ax1.set_ylabel("Periodendauerquadrat [s^2]", **plt.font)
ax1.set_title("Abstandsquadrat gegen Periodendauerquadrat", **plt.font)
plt.figtext(0.2,0.7,
            '\n a= ('+str(np.round(m,3))+' +/- '+str(np.round(em,3))+' +/- '+str(np.round(sys_err_m,3))+') s^2/m^2 \n'
            +' b= ('+str(np.round(b,3))+' +/- '+str(np.round(eb,3))+' +/- '+str(np.round(sys_err_b,3))+') s^2 \n'
            +'$\chi ^2 / ndof$= ' + str(np.round(chiq/3, 3)), **plt.font)
plt.plot(x, y, color='r')
plt.errorbar(a2, T2, xerr=sig_a2, yerr=sig_T2, fmt='.', color='b')
fig1.show()

#plotte residuen
x_r = np.array([0, 0.07])
y_r = np.array([0, 0])
X = a2
Y = np.full(a2.size, 1)
Y_err = np.full(a2.size, 1)
for i in range(a2.size):
    Y[i] = T2[i] - m * X[i] - b
    Y_err[i] = np.sqrt(sig_T2[i]**2 + (m * sig_a2[i])**2)
fig2, ax1 = plt.subplots()
plt.font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 21}
ax1.set_xlabel("Abstandsquadrat [m^2]", **plt.font)
ax1.set_ylabel("Residuen [s^2]", **plt.font)
ax1.set_title("Residuen Steiner", **plt.font)
plt.plot(x_r, y_r, color='r')
plt.errorbar(X, Y, yerr=Y_err, fmt='.', color='b')
fig2.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))