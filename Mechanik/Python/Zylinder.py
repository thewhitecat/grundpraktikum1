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

def plots(t=None,U=None,fft=0):
    if t!=None and U!=None:
        plt.subplots()
        plt.plot(t,U)
        plt.ylabel("Spannung[V]")
        plt.xlabel("Zeit[s]")
        plt.title("Rohdaten Teller")
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
        plt.title("FFT der Rohdaten vom Teller")

def tabelle(T,Tstd):
    print "\begin{table}"
    print "\caption{Zwischenergebnisse der Hohlzylindermessung.}"
    print "\begin{center}"
    print "\begin{tabular}{|c|c|c|}"
    print "\hline"
    print "Messung & ","Maxima[s] & ","Minima[] ","\\"
    print "\hline"
    for i in range(5):
        print i," & $",np.round(T[2*i],4),"\pm ",np.round(Tstd[2*i],4),"$ & $",np.round(T[2*i+1],4),"\pm ",np.round(Tstd[2*i+1],4),"$ \\"
        print "\hline"
    print "\hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\label{tab:Teller_Ergebnisse}"
    print "\end{table}"

def alles():
    teller = []
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller1.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller2.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller3.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller4.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller5.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller6.lab'))
    teller.append(p.lese_lab_datei('lab/Feder3/teller/teller7.lab'))
    D = 0.02176
    dD = 0.00025
    dDsys = np.sqrt(0.00029**2+dD**2)
    T1 = []
    T2=[]
    T2std=[]
    for i in range(len(teller)):
        t = teller[i][:,1]
        U = teller[i][:,2]
        Offset = np.mean(U)
        U=U-Offset
        peaks = a.get_peaks(t,U)
        #if i == 1:
        #    plots(t,U,fft=1)
        T1.append((t[peaks[len(peaks)-1]]-t[peaks[3]])/(len(peaks)-4)*2)
        Tmax = []
        Tmin = []
        for i in range(len(peaks)-5):
            if i%2 == 1:
                Tmax.append(t[peaks[i+4]]-t[peaks[i+2]])
            if i%2 == 0:
                Tmin.append(t[peaks[i+4]]-t[peaks[i+2]])
        T2.append(np.mean(Tmax))
        T2std.append(np.std(Tmax,ddof=1)/np.sqrt(len(Tmax)-2))
        T2.append(np.mean(Tmin))
        T2std.append(np.std(Tmin,ddof=1)/np.sqrt(len(Tmin)-2))
#    tabelle(T2,T2std)
    Tmean = np.mean(T2)
    Tstd = np.std(T2,ddof=1)/np.sqrt(len(T2)-2)
    J = (1./(4*np.pi**2))*D*(Tmean**2)
    dJ = 2./(4*np.pi**2)*D*Tmean*Tstd
    print J, dJ
    return Tmean,Tstd,T2
#alles()