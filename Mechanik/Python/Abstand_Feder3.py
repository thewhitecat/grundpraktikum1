# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:01:07 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
from auswertung_01 import*

testdata=p.lese_lab_datei('CASSY/Feder1/Quadrat/stab1.lab')
t=testdata[:,1][:-5]
U=testdata[:,2][:-5]
peaks=get_peaks(t,U)

plt.figure(1)
plt.plot(t,U)
for x in peaks:
    plt.axvline(t[x])
plt.show()

plt.figure(2)
freq,amp=p.fourier_fft(t,U)
plt.plot(freq,amp)
peak=p.peak(freq,amp,0,0.75)
plt.xlim(0,2)
plt.axvline(peak)
plt.show()



