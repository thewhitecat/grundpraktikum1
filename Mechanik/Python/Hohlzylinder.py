# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:40:35 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import auswertung_nur_Methoden as a
import Zylinder as z

def plots(t=None,U=None,fft=0):
    if t!=None and U!=None:
        plt.subplots()
        plt.plot(t,U)
        plt.ylabel("Spannung[V]")
        plt.xlabel("Zeit[s]")
        plt.title("Rohdaten Hohlzylinder")
    if fft==1:
        freq,amp=p.fourier_fft(t,U)
        freq,amp=p.untermenge_daten(freq,amp,0,3)
        plt.subplots()
        plt.plot(freq,amp)
        peak = p.peakfinder_schwerpunkt(freq,amp)
        x=plt.axvline(peak,color='r',label="{}Hz".format(np.round(peak,3)))
        plt.legend(handles=[x],bbox_to_anchor=(1, 1))
        plt.ylabel("#")
        plt.xlabel("Frequenz[Hz]")
        plt.title("FFT der Rohdaten")

hohl = []
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl1.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl2.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl3.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl4.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl5.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl6.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl7.lab'))
D = 0.02
dD = 0.0002
T1 = []
T2=[]
for i in range(len(hohl)):
    t = hohl[i][:,1]
    U = hohl[i][:,2]
    Offset = np.mean(U)
    U=U-Offset
    peaks = a.get_peaks(t,U)
    if i == 1:
        plots(t,U,fft=1)
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
Tmean = np.mean(T1)
Tstd = np.std(T1,ddof=1)/len(T1)
TTmean,TTstd,x = z.alles()
J = (1./(4*np.pi**2))*D*(Tmean**2-TTmean**2)
fehler1 = 1./(4*np.pi**2)*(Tmean**2-TTmean**2)*dD
fehler2 = 2./(4*np.pi**2)*D*Tmean*Tstd
fehler3 = 2./(4*np.pi**2)*D*TTmean*TTstd
dJ = np.sqrt(fehler1**2+fehler2**2+fehler3**2)