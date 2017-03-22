# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:42:52 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt


def daempfung (datei="19,6", eU_stat=0.001496):
    U = np.empty((5,2001))
    t = np.empty((5, 2001))
    sig_U_stat = eU_stat
    
    A0 = np.empty(5)
    sig_A0 = np.empty(5)
    delta = np.empty(5)
    sig_delta = np.empty(5)
    
    for i in range(5):
        data = p.lese_lab_datei("lab/{:s}Ohm/messung{:1d}.lab".format(datei, i+1))
        t[i] = data[:,1]
        U[i] = data[:,3]
        
        A0[i], sig_A0[i], delta[i], sig_delta[i] = p.exp_einhuellende(t[i], U[i], np.full(U[i].size, sig_U_stat))
        
        
        if (i == 1):
            plt.figure(1)
            plt.plot(t[i], U[i])
            plt.xlabel("t (s)")
            plt.ylabel("U (V)")
            
            
            x = np.arange(0, 0.02, 0.0005)
            y = A0[i]*np.exp(-delta[i]*x)
            plt.plot(x, y)
            plt.plot(x, -y)

    mean_delta, sig_mean_delta = p.gewichtetes_mittel(delta, sig_delta)
    
    return (mean_delta, sig_mean_delta)
    
    
    
    
Ordnernamen = np.array(["19,6", "28,5", "38,9", "52,2", "68,6", "90,0", "112,0", "130", "140", "150", "200"])
delta_fit = np.empty(4)
sig_delta_fit = np.empty(4)
for i in range(4):
    delta_fit[i], sig_delta_fit[i] = daempfung(datei=Ordnernamen[i])

R = np.array([19.6, 28.5, 38.9, 52.2])
sig_R_stat = np.full(4, 0.2/np.sqrt(12))


a, ea, b, eb, chi2, cov = p.lineare_regression_xy(delta_fit, R, sig_delta_fit, sig_R_stat)


plt.figure(2)
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(delta_fit, R, xerr=sig_delta_fit, yerr=sig_R_stat, fmt=".")
x = np.array([delta_fit[0]*0.90, delta_fit[-1]*1.06])
plt.xlim(x)
y = a*x+b
plt.plot(x, y)
#plt.xlabel("$\delta$ [1/s]")
plt.ylabel("R [$\Omega$]")


plt.subplot2grid((6,1),(-2,0), rowspan=2)
y = R-a*delta_fit - b
plt.errorbar(delta_fit, y, yerr = np.sqrt(sig_delta_fit**2 + a**2*sig_R_stat**2), fmt=".")
plt.xlim(x)
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("delta [1/s]")

