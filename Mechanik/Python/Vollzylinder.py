# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:39:58 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import auswertung_01 as a

def plots(t=None,U=None):
    if t!=None and U!=None:
        plt.subplots()
        plt.plot(t,U)
        

voll = []
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll1.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll2.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll3.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll4.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll5.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll6.lab'))
voll.append(p.lese_lab_datei('lab/Feder3/voll/voll7.lab'))
D = 0.02
T = []
for i in range(len(voll)):
    t = voll[i][:,1]
    U = voll[i][:,2]
    Offset = np.mean(U)
    U=U-Offset
    peaks = a.get_peaks(t,U)
    if i == 1:
        plots(t,U)
    T.append((t[peaks[len(peaks)-1]]-t[peaks[2]])/(len(peaks)-2)*2)
Tmean = np.mean(T)
Tstd = np.std(T,ddof=1)/len(T)
J =1/(4*np.pi**2) * D * Tmean**2