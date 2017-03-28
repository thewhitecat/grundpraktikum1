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

def tabelle(T,Tstd):
    print "\begin{table}"
    print "\caption{Zwischenergebnisse der Hohlzylindermessung.}"
    print "\begin{center}"
    print "\begin{tabular}{|c|c|c|}"
    print "\hline"
    print "Messung & ","Maxima & ","Minima ","\\"
    print "\hline"
    for i in range(5):
        print i," & $",np.round(T[2*i],3),"\pm ",np.round(Tstd[2*i],3),"$ & $",np.round(T[2*i+1],3),"\pm ",np.round(Tstd[2*i+1],3),"$ \\"
        print "\hline"
    print "\hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\label{tab:Teller_Ergebnisse}"
    print "\end{table}"

hohl = []
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl1.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl2.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl3.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl4.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl5.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl6.lab'))
hohl.append(p.lese_lab_datei('lab/Feder3/Hohlzylinder/hohl7.lab'))
D = 0.02176
dD = 0.00025
dDsys = np.sqrt(0.00029**2+dD**2)
T1 = []
T2=[]
T2std=[]
for i in range(len(hohl)):
    t = hohl[i][:,1]
    U = hohl[i][:,2]
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

#tabelle(T2,T2std)
Tmean = np.mean(T1)
Tstd = np.std(T1,ddof=1)/np.sqrt(len(T1)-2)
TTmean,TTstd,x = z.alles()
J = (1./(4*np.pi**2))*D*(Tmean**2-TTmean**2)
fehler1 = 1./(4*np.pi**2)*(Tmean**2-TTmean**2)*dDsys
fehler2 = 2./(4*np.pi**2)*D*Tmean*Tstd
fehler3 = 2./(4*np.pi**2)*D*TTmean*TTstd
dJ = np.sqrt(fehler2**2+fehler3**2)
raussen = np.array([9.01,9.02,9.014,9.012,9.022,9.014,9.018,9.012])/100
rinnen = np.array([8.6,8.6,8.585,8.575,8.58,8.59,8.6,8.59])/100
raussenm = np.mean(raussen)/2
rinnenm = np.mean(rinnen)/2
rstat = 0.001/(100*np.sqrt(12))
rsys = 0.05/1000
m = 0.3487
mstat = 0.0001/np.sqrt(12)
msys = 0.0001
JTheo = m*(rinnenm**2+raussenm**2)/2
Jstat = np.sqrt(((rinnenm**2+raussenm**2)/2 * mstat)**2+(2*m*rinnenm*rstat)**2+(2*m*raussenm*rstat)**2)
Jsys = np.sqrt(((rinnenm**2+raussenm**2)/2 * msys)**2+(2*m*rinnenm*rsys+2*m*raussenm*rsys)**2)