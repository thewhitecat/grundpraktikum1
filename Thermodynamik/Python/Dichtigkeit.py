# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:05:49 2017

@author: grldm
"""

import Praktikum as prak
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt
import Rauschmessung as Rm

start_time=timeit.default_timer()

#Lese alle Datensätze ein
M_S_1 = p.lese_lab_datei('lab/Dichtigkeitsmessung_vorher.lab')
p_v = M_S_1[:, 4]
t_v = M_S_1[:, 1]

M_S_2 = p.lese_lab_datei('lab/Dichtigkeitsmessung_nachher_2.lab')
p_n = M_S_2[:, 4]
t_n = M_S_1[:, 1]

#lineare Regression an Druckverlauf für Leckrate und Fehler auf Leckrate
def func(t, p):
    a, var, c = Rm.mean(p)
    sig_einzel = np.sqrt(var**2 + 0.75**2)
    p_err = np.full(p.size, sig_einzel)
    rate, rate_var, b, eb, chiq, corr = prak.lineare_regression(t, p, p_err)
    return rate, rate_var, b, eb, chiq, var

leckrate_v, Fehler_v, b_v, eb_v, chiq_v, var_v = func(t_v, p_v)
leckrate_n, Fehler_n, b_n, eb_n, chiq_n, var_n = func(t_n, p_n)

#plotte Residuen
X = t_v
Y = np.full(p_v.size, 1)
for i in range(p_v.size):
    Y[i] = p_v[i] - leckrate_v * t_v[i] - b_v
Y_err = np.full(p_v.size, np.sqrt(var_v**2 + 0.75**2))
fig1, ax1 = plt.subplots()
ax1.set_xlabel("Zeit [s]")
ax1.set_ylabel("Abweichung: gemessener Wert - lineare Regression")
plt.errorbar(X, Y, yerr=Y_err, fmt='.')
fig1.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))