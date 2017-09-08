# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 16:11:08 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data_raw = np.genfromtxt('Druck_B.txt', delimiter = ',', skip_header = 1)

m = data_raw[:,0]
sol = []
chiq = []
a_linreg = []
ea_linreg = []

for i in range(len(data_raw[0,:])-1):
    x, y = AM.nan_aus_daten(m, data_raw[:,i+1])
    ey = np.full(len(y), 1/np.sqrt(12))
    ex = np.full(len(x), 0.2/np.sqrt(12))
    sol += [p.lineare_regression_xy(np.array(x), np.array(y), ex, ey)]
    chiq += [sol[i][4] / (len(x)-2)]
    a_linreg += [sol[i][0]]
    ea_linreg += [sol[i][1]]

#print sol
#print chiq

l = 0.01
wavelength = 526.2 * 10**(-9)
wavelength_std = 1.2 * 10**(-9)

a, ea = p.gewichtetes_mittel(np.array(a_linreg), np.array(ea_linreg))
a_std = np.std(np.array(a_linreg))

dn_dP = np.abs(1/a * wavelength / (2 * l))
sig_dn_dP = dn_dP * np.sqrt((a_std / a)**2 + (wavelength_std / wavelength)**2)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))