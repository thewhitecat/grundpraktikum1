# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:52:52 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

data = []
data.append(p.lese_lab_datei('lab/Gegensinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gegensinnig_03.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_01.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_02.lab'))
data.append(p.lese_lab_datei('lab/Gleichsinnig_03.lab'))

for data in data:
    t = data[:,1]
    U1 = data[:,2]
    U2 = data[:,3]
    freq,amp = p.fourier_fft(t,U1)
    freq = p.untermenge_daten(TO BE CONTIUNED)
    plt.subplots()
    plt.plot(freq,amp)