# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 09:40:05 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import pylab as pyl


daten_druckknoten = p.lese_lab_datei("cassy\Druckknoten1.lab")

spannung = daten_druckknoten[:,2]
widerstand = daten_druckknoten[:,3]


plt.figure(1)
plt.subplot(1, 1, 1)
plt.plot(widerstand, spannung)

peak1 = 1.8705

peak2 = 1.3285

sigma = 0.005

sigma_f = 1.4

v = 2*(peak1-peak2)*0.1597*2017
sigma_v = v*np.sqrt( (2*sigma/(peak1-peak2))**2 + (sigma_f/2017)**2 )

plt.plot([peak1, peak1], [0,1])
plt.plot([peak2, peak2], [0,1])

print(v)
print(sigma_v)