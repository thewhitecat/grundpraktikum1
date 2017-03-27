# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:31:26 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import auswertung_nur_Methoden as a

def plots(t=None,U=None):
    if t!=None and U!=None:
        plt.subplots()
        plt.plot(t,U)
        
def alles():
    teller = []
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller1.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller2.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller3.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller4.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller5.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller6.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller7.lab'))
    D = 0.02
    T1 = []
    T2=[]
    for i in range(len(teller)):
        t = teller[i][:,1]
        U = teller[i][:,2]
        Offset = np.mean(U)
        U=U-Offset
        peaks = a.get_peaks(t,U)
        #if i == 1:
        #    plots(t,U)
        T1.append((t[peaks[len(peaks)-1]]-t[peaks[3]])/(len(peaks)-4)*2)
        Tmax = []
        Tmin = []
        for i in range(len(peaks)-5):
            if i%2 == 1:
                Tmax.append(t[peaks[i+4]]-t[peaks[i+2]])
            if i%2 == 0:
                Tmin.append(t[peaks[i+4]]-t[peaks[i+2]])
        T2.append(np.mean(Tmax))
        T2.append(np.mean(Tmin))
    Tmean = np.mean(T2)
    Tstd = np.std(T2,ddof=1)/len(T2)
    return Tmean,Tstd
    