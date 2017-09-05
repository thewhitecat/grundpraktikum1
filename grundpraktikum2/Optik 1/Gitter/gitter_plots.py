# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 15:11:11 2017

@author: Sebastian
"""

import numpy as np
import matplotlib.pyplot as plt

a = 1658.9
grad = lambda x: 180/np.pi *x
winkel = lambda x: grad(np.arcsin(x/a))

messung = np.array([405.32, 436.74, 547.06, 578.01, 580.24])
std = np.array([2.15, 0.86, 1.06, 1.17, 1.29])

literatur = {'BlueViolet':404.66, 'DarkMagenta':435.83, 'Lime':546.07, 'DarkOrange':576.96, 'Orange':579.07}

plt.figure(1, [8,3])
plt.xlabel("Wellenlaenge [nm]")
plt.ylim(0.8,2.3)
plt.errorbar(winkel(messung), winkel(messung)/11, xerr=np.sqrt(messung/300)*std*grad(1/(a*np.sqrt(1-(winkel(messung)/a)**2))), fmt=".")
for key, value in literatur.iteritems():
    plt.axvline(x=winkel(value), color=key)