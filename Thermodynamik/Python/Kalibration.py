# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:15:04 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt

start_time=timeit.default_timer()

#Lese alle Datensätze ein
M_S_1 = p.lese_lab_datei('Lab/Temperatur_Eiswasser.lab')
T_E = M_S_1[:, 2]

M_S_2 = p.lese_lab_datei('Lab/Temperatur_siedend.lab')
T_S = M_S_2[:, 2]

def func(T_E, T_S):
    #Mittelwert und Standardabweichung für Temperaturen
    T_E_mw = np.mean(T_E)
    T_E_std = np.std(T_E)
    T_S_mw = np.mean(T_S)
    T_S_std = np.std(T_S)

    #Bestimme Steigung und Offset
    m = 100/(T_S_mw - T_E_mw)
    T_0 = 100 - m * T_S_mw

    #Bestimme Fehler auf Steigung und Offset
    sig_m = np.sqrt(((T_S_std*100)/(T_S_mw - T_E_mw)**2)**2 + ((T_E_std*100)/(T_S_mw - T_E_mw)**2)**2)
    sig_T_0 = np.sqrt(sig_m**2 * T_S_std**2)
    return m, sig_m, T_0, sig_T_0

m, sig_m, T_0, sig_T_0 = func(T_E, T_S[789:1089])

print("Steigung der Geraden: ", m, " +/- ", sig_m)
print("Offset der Geraden: ", T_0, " +/- ", sig_T_0)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))