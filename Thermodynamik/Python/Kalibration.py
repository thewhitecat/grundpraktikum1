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
import Rauschmessung

start_time=timeit.default_timer()

#Lese alle Datensätze ein
M_S_1 = p.lese_lab_datei('lab/Temperatur_Eiswasser.lab')
#M_S_1 = p.lese_lab_datei('CASSY/Rauschmessungen.lab')
T_E = M_S_1[:, 2]
#T_E = M_S_1[:, 3]

M_S_2 = p.lese_lab_datei('lab/Temperatur_siedend.lab')
#M_S_2 = p.lese_lab_datei('CASSY/Temperatur_siedend.lab')
T_S = M_S_2[:, 2]
#T_S = M_S_2[:, 3]

T_S = T_S[730:]

def func(T_E, T_S):
    #Mittelwert und Standardabweichung für Temperaturen
    T_E_mw,x,T_E_std = Rauschmessung.mean(T_E)
    T_S_mw,x,T_S_std = Rauschmessung.mean(T_S)
    print np.round(T_E_mw,3),np.round(T_E_std,3)
    print np.round(T_S_mw,3),np.round(T_S_std,3)
    
    #Bestimme Steigung und Offset
    m = 99.72/(T_S_mw - T_E_mw)
    T_0 = 99.72 - m * T_S_mw

    #Bestimme Fehler auf Steigung und Offset
    sig_m = m * np.sqrt(((T_S_std*99.72)/(T_S_mw - T_E_mw)**2)**2 + ((T_E_std*99.72 )/(T_S_mw - T_E_mw)**2)**2)
    sig_T_0 = T_0 * np.sqrt((sig_m/m)**2 + (T_S_std/T_S_mw)**2)
    return m, sig_m, T_0, sig_T_0

m, sig_m, T_0, sig_T_0 = func(T_E, T_S)

print("Steigung der Geraden: ", m, " +/- ", sig_m)
print("Offset der Geraden: ", T_0, " +/- ", sig_T_0)
print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))

def graphen():
    x=np.linspace(-20,120,100)
    y=m*x+T_0
    plt.figure()
    plt.plot(x,y)
    x2=[np.mean(T_E),np.mean(T_S)]
    y2=[0,100]
    err=[np.std(T_E),np.std(T_S)]
    plt.errorbar(x2,y2,yerr=err,fmt='o')
    plt.xlabel('T(gemessen)/C')
    plt.ylabel('T(erwartet)/C')
    plt.title('Temperatur')
    plt.figtext(0.2,0.7,'Steigung: '+ str(np.round(m,4)) + ' +/- '+ str(np.round(sig_m,4))+'\n'
                +'Offset: '+ str(np.round(T_0,4)) + ' +/- '+str(np.round(sig_T_0,4)))
    
graphen()