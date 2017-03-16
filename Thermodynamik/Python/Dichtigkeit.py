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
M_S_1 = prak.lese_lab_datei('lab/Dichtigkeitsmessung_vorher.lab')
p_v = M_S_1[:, 4]
t_v = M_S_1[:, 1]

M_S_2 = prak.lese_lab_datei('lab/Dichtigkeitsmessung_nachher_2.lab')
p_n = M_S_2[:, 4]
t_n = M_S_2[:, 1]

#lineare Regression an Druckverlauf für Leckrate und Fehler auf Leckrate
def func(t, p):
    a, var, c = Rm.mean(p)
    sig_einzel = np.sqrt(var**2 + 0.75**2)
    p_err = np.full(p.size, sig_einzel)
    rate, rate_var, b, eb, chiq, corr = prak.lineare_regression(t, p, p_err)
    return rate, rate_var, b, eb, chiq, var

leckrate_v, Fehler_v, b_v, eb_v, chiq_v, var_v = func(t_v, p_v)
leckrate_n, Fehler_n, b_n, eb_n, chiq_n, var_n = func(t_n, p_n)

#plotte Residuen für Messung vorher
X = t_v
Y = np.full(p_v.size, 1)
for i in range(p_v.size):
    Y[i] = p_v[i] - leckrate_v * t_v[i] - b_v
Y_err = np.full(p_v.size, np.sqrt(var_v**2 + 0.75**2))
fig1, ax1 = plt.subplots()
ax1.set_xlabel("Zeit [s]")
ax1.set_ylabel("Abweichung: gemessener Wert - lineare Regression")
ax1.set_title("Residuen Dichtigkeitsmessung vorher")
plt.errorbar(X, Y, yerr=Y_err, fmt='.')
fig1.show()

#plotte Residuen für Messung nachher
X_n = t_n
Y_n = np.full(p_n.size, 1)
for i in range(p_n.size):
    Y_n[i] = p_n[i] - leckrate_n * t_n[i] - b_n
Y_n_err = np.full(p_n.size, np.sqrt(var_n**2 + 0.75**2))
fig2, ax1 = plt.subplots()
ax1.set_xlabel("Zeit [s]")
ax1.set_ylabel("Abweichung: gemessener Wert - lineare Regression")
ax1.set_title("Residuen Dichtigkeitsmessung nachher")
plt.errorbar(X_n, Y_n, yerr=Y_n_err, fmt='.')
fig2.show()

#plotte lineare Regression an Messung vorher
x = np.array([0, 300])
y = leckrate_v * x + b_v
sig_einzel = np.sqrt(Fehler_v**2 + 0.75**2)
p_err = np.full(p_v.size, sig_einzel)
fig3, ax3 = plt.subplots()
ax3.set_xlabel("Zeit [s]")
ax3.set_ylabel("Druck [mbar]")
ax3.set_title("Dichtigkeitsmessung vor Hauptversuch")
plt.errorbar(t_v, p_v, yerr=p_err, fmt='.')
plt.plot(x, y)
fig3.show()

#plotte lineare Regression an Messung nachher
x = np.array([0, 300])
y = leckrate_n * x + b_n
sig_einzel = np.sqrt(Fehler_n**2 + 0.75**2)
p_n_err = np.full(p_n.size, sig_einzel)
fig4, ax3 = plt.subplots()
ax3.set_xlabel("Zeit [s]")
ax3.set_ylabel("Druck [mbar]")
ax3.set_title("Dichtigkeitsmessung nach Hauptversuch")
plt.errorbar(t_n, p_n, yerr=p_n_err, fmt='.')
plt.plot(x, y)
fig4.show()

print("Leckrate vorher: (", leckrate_v * 60, " +/- ", Fehler_v * 60, ") hPA/min")
print("Leckrate nachher: (", leckrate_n * 60, " +/- ", Fehler_n * 60, ") hPA/min")

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))