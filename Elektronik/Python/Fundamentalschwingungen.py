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
        line1 = plt.axvline(x=707.9,color='r',label='f+ = (707.9+/-1.8)Hz')
        line2 = plt.axvline(x=815.1,color='g',label='f- = (815.1+/-1.8)Hz')
        plt.legend(handles = [line1,line2],bbox_to_anchor=(0.45, 1))
    if t!=None and U1!=None:
        t,U1 = p.untermenge_daten(t,U1,0,0.08)
        plt.subplots()
        plt.plot(t,U1)
        plt.ylabel("Spannung[V]")
        plt.xlabel("Zeit[s]")
        plt.title("Rohdaten")
    if t!=None and U2!=None:
        t,U2 = p.untermenge_daten(t,U2,0,0.08)
        plt.subplots()
        plt.plot(t,U2)
        plt.ylabel("Spannung[V]")
        plt.xlabel("Zeit[s]")
        plt.title("Rohdaten")

data = []
data.append(p.lese_lab_datei('lab/Gegensinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_03.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_03.lab'))

peak_p1 = []#peak gleichsinnig
peak_p1var = []#peak gleichsinnig
peak_g1 = []#peak gegensinnig
peak_g1var = []#peak gleichsinnig
peak_p2 = []#peak gleichsinnig
peak_p2var = []#peak gleichsinnig
peak_g2 = []#peak gegensinnig
peak_g2var = []#peak gleichsinnig
for i in range(len(data)):
 #   i +=3
    dat = data[i]
    t = dat[:,1]
    U1 = dat[:,2]
    U2 = dat[:,3]
    freq,amp = p.fourier_fft(t,U1)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    if i == 1:
        pictures(freq,amp)
    if i < 3:
        freq1,amp1 = p.untermenge_daten(freq,amp,680,780)
        freq2,amp2 = p.untermenge_daten(freq,amp,780,850)
        
        sp = p.peakfinder_schwerpunkt(freq1,amp1)
        sp2 = p.peak(freq1,amp1,680,780)
        sp3 = freq[np.argmax(amp)]
        sp3var = (freq[np.argmax(amp)+1]-freq[np.argmax(amp)-1])/(2*np.sqrt(12))
        peak_p1.append(sp2)
        peak_p1var.append(sp3var)
        #sp = p.peakfinder_schwerpunkt(freq2,amp2)
        #if sp>=780 and sp<=820:
        #    peak_g1.append(sp)
    if i >= 3:
        freq1,amp1 = p.untermenge_daten(freq,amp,780,850)
        freq2,amp2 = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq1,amp1)
        sp2 = p.peak(freq1,amp1,780,850)
        sp3 = freq1[np.argmax(amp1)]
        sp3var = (freq[np.argmax(amp)+1]-freq[np.argmax(amp)-1])/(2*np.sqrt(12))
        peak_g1.append(sp2)
        peak_g1var.append(sp3var)
        #sp = p.peakfinder_schwerpunkt(freq2,amp2)
        #if sp>=680 and sp<=780:
       #    peak_p1.append(sp)
        
    freq,amp = p.fourier_fft(t,U2)
    freq,amp = p.untermenge_daten(freq,amp,200,1000)
    if i == 4:
        pictures(freq,amp)
        test1, test2 = freq,amp
    if i < 3:
        freq1,amp1 = p.untermenge_daten(freq,amp,680,780)
        freq2,amp2 = p.untermenge_daten(freq,amp,780,850)
        sp = p.peakfinder_schwerpunkt(freq1,amp1)
        sp2 = p.peak(freq1,amp1,680,780)
        sp3 = freq[np.argmax(amp)]
        sp3var = (freq[np.argmax(amp)+1]-freq[np.argmax(amp)-1])/(2*np.sqrt(12))
        peak_p2.append(sp)
        peak_p2var.append(sp3var)
        #sp = p.peakfinder_schwerpunkt(freq2,amp2)
        #if sp>=680 and sp<=780:
        #    peak_g2.append(sp)
    if i >= 3:
        freq1,amp1 = p.untermenge_daten(freq,amp,780,850)
        freq2,amp2 = p.untermenge_daten(freq,amp,680,780)
        sp = p.peakfinder_schwerpunkt(freq1,amp1)
        sp2 = p.peak(freq1,amp1,780,850)
        sp3 = freq[np.argmax(amp)]
        sp3var = (freq[np.argmax(amp)+1]-freq[np.argmax(amp)-1])/(2*np.sqrt(12))
        peak_g2.append(sp)
        peak_g2var.append(sp3var)
        #sp = p.peakfinder_schwerpunkt(freq2,amp2)
        #if sp>=680 and sp<=780:
         #   peak_p2.append(sp)

ppmu1,ppstd1=np.mean(peak_p1),np.std(peak_p1)/len(peak_p1)
pgmu1,pgstd1=np.mean(peak_g1),np.std(peak_g1)/len(peak_g1)
ppmu2,ppstd2=np.mean(peak_p2),np.std(peak_p2)/len(peak_p2)
pgmu2,pgstd2=np.mean(peak_g2),np.std(peak_g2)/len(peak_g2)
ppstd1 = np.sqrt(ppstd1**2+1.8**2)
pgstd1 = np.sqrt(pgstd1**2+1.8**2)
ppstd2 = np.sqrt(ppstd2**2+1.8**2)
pgstd2 = np.sqrt(pgstd2**2+1.8**2)

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









