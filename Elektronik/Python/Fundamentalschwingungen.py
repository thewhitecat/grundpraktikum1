# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:52:52 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

def pictures(freq=None,amp=None,t=None,U1=None,U2=None):
    if freq!=None and amp!=None:
        plt.subplots()
        plt.plot(freq,amp)
        plt.ylabel("#")
        plt.xlabel("Frequenz[Hz]")
        plt.title("Freqenzspektrum")
    if t!=None and U1!=None:
        t,U1 = p.untermenge_daten(t,U1,0,0.08)
        plt.subplots()
        plt.plot(t,U1)
        plt.xlabel("Spannung[V]")
        plt.ylabel("Zeit[s]")
        plt.title("Rohdaten")
    if t!=None and U2!=None:
        t,U2 = p.untermenge_daten(t,U2,0,0.08)
        plt.subplots()
        plt.plot(t,U2)
        plt.xlabel("Spannung[V]")
        plt.ylabel("Zeit[s]")
        plt.title("Rohdaten")

data = []
data.append(p.lese_lab_datei('lab/Gegensinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_03.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_03.lab'))

peak_p1 = []#peak gleichsinnig
peak_g1 = []#peak gegensinnig
peak_p2 = []#peak gleichsinnig
peak_g2 = []#peak gegensinnig
for i in range(len(data)):
 #   i +=3
    dat = data[i]
    t = dat[:,1]
    U1 = dat[:,2]
    U2 = dat[:,3]
    freq,amp = p.fourier_fft(t,U1)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    if i == 0:
        pictures(freq,amp,t=t,U1=U1)
    if i < 3:
        freq,amp = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,680,780)
        peak_p1.append(sp2)
    if i >= 3:
        freq,amp = p.untermenge_daten(freq,amp,780,850)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,780,840)
        peak_g1.append(sp2)
        
    freq,amp = p.fourier_fft(t,U2)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    if i == 4:
        pictures(freq,amp,t=t,U2=U2)
    if i < 3:
        freq,amp = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,680,780)
        peak_p2.append(sp)
    if i >= 3:
        freq,amp = p.untermenge_daten(freq,amp,780,850)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,750,840)
        peak_g2.append(sp)

ppmu1,ppstd1=np.mean(peak_p1),np.std(peak_p1)/len(peak_p1)
pgmu1,pgstd1=np.mean(peak_g1),np.std(peak_g1)/len(peak_g1)
ppmu2,ppstd2=np.mean(peak_p2),np.std(peak_p2)/len(peak_p2)
pgmu2,pgstd2=np.mean(peak_g2),np.std(peak_g2)/len(peak_g2)

k1 = (pgmu1**2 - ppmu1**2)/(ppmu1**2 + pgmu1**2)
zahl=(pgmu1**2 - ppmu1**2)
nenn=(ppmu1**2 + pgmu1**2)
dk1 = np.sqrt(((1/nenn - zahl/nenn**2)*2*pgmu1*pgstd1)**2 + ((-1/nenn - zahl/nenn**2)*2*ppmu1*ppstd1)**2)
k2 = (pgmu2**2 - ppmu2**2)/(ppmu2**2 + pgmu2**2)
zahl=(pgmu2**2 - ppmu2**2)
nenn=(ppmu2**2 + pgmu2**2)
dk2 = np.sqrt(((1/nenn - zahl/nenn**2)*2*pgmu2*pgstd2)**2 + ((-1/nenn - zahl/nenn**2)*2*ppmu2*ppstd2)**2)
print k1,dk1
print k2,dk2
print ppmu1,ppstd1
print ppmu2,ppstd2
print pgmu1,pgstd1
print pgmu2,pgstd2

kmittel,kstd = p.gewichtetes_mittel([k1,k2],np.array([dk1,dk2]))
print kmittel,kstd









