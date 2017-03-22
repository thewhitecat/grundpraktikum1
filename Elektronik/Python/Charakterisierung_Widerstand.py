# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:41:23 2017

@author: grldm
"""

import Praktikum as prak
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt

start_time=timeit.default_timer()

#Lese Daten ein
M_S_1 = prak.lese_lab_datei('lab/100Ohm_ges.lab')
index = M_S_1[:, 0]
U = M_S_1[:, 3]
I = M_S_1[:, 2]

#jeweils mittelwert und standardabweichung bestimmen
def mw_std_best(ind, x):
    a = []
    for i in range(len(x)):
        if ind[i] == 1:
            a.append(i)
    mw = []
    std = []
    for i in range(len(a)-2):
        mw.append(np.mean(x[a[i]:a[i+1]-1]))
        std.append(np.std(x[a[i]:a[i+1]-1]))
    mw.append(np.mean(x[a[len(a)-1]:]))
    std.append(np.std(x[a[len(a)-1]:]))
    return np.array(mw), np.array(std)

mw_U, std_U = mw_std_best(index, U)
mw_I, std_I = mw_std_best(index, I)

#lineare Regression
R, dR_stat, b_R, eb_R, chiq_R, cov = prak.lineare_regression_xy(mw_I, mw_U, std_I, std_U)

#verschiebemethode
def verschiebemethode(x, y, ind, R):
    x_o = np.empty(len(x))
    x_u = np.empty(len(x))
    y_o = np.empty(len(y))
    y_u = np.empty(len(y))
    for i in range(len(x)):
        x_o[i] = x[i] + 0.01 * x[i] + 0.005 * 10
        x_u[i] = x[i] - 0.01 * x[i] - 0.005 * 10
        y_o[i] = y[i] + 0.02 * y[i] + 0.005 * 0.3
        y_u[i] = y[i] - 0.02 * y[i] - 0.005 * 0.3
    mw_x_o, std_x_o = mw_std_best(ind, x_o)
    mw_x_u, std_x_u = mw_std_best(ind, x_u)
    mw_y, std_y = mw_std_best(index, y)
    R_x_o, ea, b, eb, chiq, cov = prak.lineare_regression_xy(mw_y, mw_x_o, std_y, std_x_o)
    R_x_u, ea, b, eb, chiq, cov = prak.lineare_regression_xy(mw_y, mw_x_u, std_y, std_x_u)
    mw_y_o, std_y_o = mw_std_best(ind, y_o)
    mw_y_u, std_y_u = mw_std_best(ind, y_u)
    mw_x, std_x = mw_std_best(index, x)
    R_y_o, ea, b, eb, chiq, cov = prak.lineare_regression_xy(mw_y_o, mw_x, std_y_o, std_x)
    R_y_u, ea, b, eb, chiq, cov = prak.lineare_regression_xy(mw_y_u, mw_x, std_y_u, std_x)
    R_sys = np.sqrt(((np.sqrt((R_x_u - R)**2) + np.sqrt((R_x_o - R)**2))/2)**2 + ((np.sqrt((R_y_u - R)**2) + np.sqrt((R_y_o - R)**2))/2)**2)
    return R_sys

R_sys = verschiebemethode(U, I, index, R)

#statistischer Fehler auf Strom und Spannung aus Rauschmessung
stat_I = np.mean(std_I)
stat_U = np.mean(std_U)

#plotte lineare Regression
x = np.array([-0.09, 0])
y = R * x + b_R
fig1, ax1 = plt.subplots()
plt.font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 21}
ax1.set_xlabel("Strom [A]", **plt.font)
ax1.set_ylabel("Spannung [V]", **plt.font)
ax1.set_title("Strom gegen Spannung", **plt.font)
plt.figtext(0.5,0.7,
            '\n a= ('+str(np.round(R,3))+' +/- '+str(np.round(dR_stat,3))+') Ohm\n'
            +' b= ('+str(np.round(b_R,3))+' +/- '+str(np.round(eb_R,3))+') V\n'
            +'$\chi ^2 / ndof$= ' + str(chiq_R/(mw_I.size-2)), **plt.font)
plt.plot(x, y, color='r')
plt.errorbar(mw_I, mw_U, xerr=std_I, yerr=std_U, fmt='.', color='b')
fig1.show()

#plotte Residuen
x_r = np.array([-0.09, 0])
y_r = np.array([0, 0])
X = mw_I
Y = np.full(mw_I.size, 1)
Y_err = np.full(mw_I.size, 1)
for i in range(mw_I.size):
    Y[i] = mw_U[i] - R * X[i] - b_R
    Y_err[i] = np.sqrt(std_U[i]**2 + (R * std_I[i])**2)
fig2, ax1 = plt.subplots()
plt.font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 21}
ax1.set_xlabel("Zeit [s]", **plt.font)
ax1.set_ylabel("Residuen [hPa]", **plt.font)
ax1.set_title("Residuen Charakterisierung Widerstand", **plt.font)
plt.plot(x_r, y_r, color='r')
plt.errorbar(X, Y, yerr=Y_err, fmt='.', color='b')
fig2.show()

print("Widerstand: ", np.sqrt(R**2))
print("Statistischer Fehler: ", dR_stat)
print("Systematischer Fehler: ", R_sys)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))