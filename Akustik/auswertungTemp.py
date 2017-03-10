# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:37:06 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import  pylab as pyl

temperaturdaten_anfang = p.lese_lab_datei("cassy\Temperatur.lab")[:,2]

temp_anfang = np.mean(temperaturdaten_anfang)
sigma_temp_anfang = np.std(temperaturdaten_anfang, ddof = 1)/temperaturdaten_anfang.size
schallgeschwindigkeit_anfang = 331.6 + 0.6*temp_anfang
sigma_v_anfang = schallgeschwindigkeit_anfang*sigma_temp_anfang/temp_anfang

print("mu={:f}\nsigma={:f}".format(schallgeschwindigkeit_anfang, sigma_v_anfang))

plt.figure(1)
plt.subplot(1,1,1)
plt.title("Temperatur Anfang")
plt.hist(temperaturdaten_anfang, bins=20)
plt.figtext(0.6, 0.7, "$\mu _T = {:2.3f}C$\n$\sigma _T = {:2.3f}C$".format(temp_anfang, sigma_temp_anfang))





temperaturdaten_resonanz = p.lese_lab_datei("cassy\Temp vor Resonanz.lab")[:,2]

temp_resonanz = np.mean(temperaturdaten_resonanz)
sigma_temp_resonanz = np.std(temperaturdaten_resonanz, ddof = 1)/temperaturdaten_resonanz.size
schallgeschwindigkeit_resonanz = 331.6 + 0.6*temp_resonanz
sigma_v_resonanz = schallgeschwindigkeit_resonanz*sigma_temp_resonanz/temp_resonanz

print("mu={:f}\nsigma={:f}".format(schallgeschwindigkeit_resonanz, sigma_v_resonanz))

plt.figure(2)
plt.subplot(1,1,1)
plt.title("Temperatur Resonanz")
plt.hist(temperaturdaten_resonanz, bins=20)
plt.figtext(0.6, 0.7, "$\mu _T = {:2.3f}C$\n$\sigma _T = {:2.3f}C$".format(temp_resonanz, sigma_temp_resonanz))