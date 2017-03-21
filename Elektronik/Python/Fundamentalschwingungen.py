# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:52:52 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

def pictures(freq=None,amp=None):
    if freq!=None and amp!=None:
        plt.subplots()
        plt.plot(freq,amp)
        plt.xlabel("#")
        plt.ylabel("Frequenz[Hz]")
        plt.title("Freqenzspektrum")

data = []
data.append(p.lese_lab_datei('lab/Gegensinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_03.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_03.lab'))

peak_p = []#peak gleichsinnig
peak_g = []#peak gegensinnig
for i in range(len(data)):
 #   i +=3
    dat = data[i]
    t = dat[:,1]
    U1 = dat[:,2]
    U2 = dat[:,3]
    freq,amp = p.fourier_fft(t,U1)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    #pictures(freq,amp)
    if i < 3:
        freq,amp = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,680,780)
        peak_p.append(sp2)
    if i >= 3:
        freq,amp = p.untermenge_daten(freq,amp,780,850)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,780,840)
        peak_g.append(sp2)
        
    freq,amp = p.fourier_fft(t,U2)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    #pictures(freq,amp)
    if i < 3:
        freq,amp = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,680,780)
        peak_p.append(sp)
    if i >= 3:
        freq,amp = p.untermenge_daten(freq,amp,780,850)
        sp = p.peakfinder_schwerpunkt(freq,amp)
        sp2 = p.peak(freq,amp,750,840)
        peak_g.append(sp)

ppmu,ppstd=np.mean(peak_p),np.std(peak_p)/len(peak_p)
pgmu,pgstd=np.mean(peak_g),np.std(peak_g)/len(peak_g)

k = (pgmu**2 - ppmu**2)/(ppmu**2 + pgmu**2)
zahl=(pgmu**2 - ppmu**2)
nenn=(ppmu**2 + pgmu**2)
dk = np.sqrt(((1/nenn - zahl/nenn**2)*2*pgmu*pgstd)**2 + ((-1/nenn - zahl/nenn**2)*2*ppmu*ppstd)**2)
print k,dk
print ppmu,ppstd
print pgmu,pgstd









