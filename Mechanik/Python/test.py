# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:27:45 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

import auswertung_02 as a



delta = np.empty(7)
sigma_stat = np.empty(7)
sigma_sys = np.empty(7)

T = np.empty(7)
sigma_T = np.empty(7)

index_lenght = 40
for i in range(1,8):
    datei = "lab/Feder3/Hohlzylinder/hohl{:1d}.lab".format(i)
    data = p.lese_lab_datei(datei)
    t = data[:,1]
    U = data[:,2]
    
    U, t = p.untermenge_daten(U, t, -2, 2)
    
    U = U - np.mean(U[-U.size/5:])
    
    indizes = a.get_peaks(t, U)
    
    if indizes.size > index_lenght:
        indizes = indizes[:index_lenght]
    print indizes.size
    
    delta[i-1], sigma_stat[i-1], sigma_sys[i-1] = a.daempfung(t, U, indizes, i)
    
    T[i-1], sigma_T[i-1] = a.periodendauer(datei)
    
    
print delta, sigma_stat, sigma_sys
print T, sigma_T


omega0 = 2*np.pi/T
sigma_omega0 = 2*np.pi*sigma_T/T**2

print np.sqrt(omega0**2 - delta**2)

omega = np.sqrt(omega0**2 - delta**2)
sig_temp = np.sqrt( (2*omega0*sigma_omega0)**2 + (2*np.sqrt(sigma_stat**2 + sigma_sys**2)*delta)**2 )
sigma_omega = sig_temp/(2 * omega)

T_neu = 2*np.pi/omega
sigma_T_neu = 2*np.pi*sigma_omega/omega**2