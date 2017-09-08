# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 15:05:48 2017

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
P_mean = []
P_std = []
for i in range(len(data_raw[:,0])):
    mw = np.mean(AM.nan_aus_array(data_raw[i,:][1:]))
    std = np.std(AM.nan_aus_array(data_raw[i,:][1:]))
    P_mean += [mw]
    P_std += [std]

P_std[0] = np.mean(np.array(P_std[1:]))

sol = p.lineare_regression(np.array(m), np.array(P_mean), np.array(P_std))

#plotte schön
plt.figure(1)
ax1=plt.subplot(211)
x = np.array([m[0], m[-1]])
y = sol[0] * x + sol[2]
ax1.set_ylabel("P [hPa]")
#ax1.set_title("")
plt.figtext(0.2,0.7,
            '\n a= ('+str(np.round(sol[0],6))+' +/- '+str(np.round(sol[1],8))+') 1/nm \n'
            +' b= ('+str(np.round(sol[2],6))+' +/- '+str(np.round(sol[3],6))+')  \n'
            +'$\chi ^2 / ndof$= ' + str(np.round(sol[4]/7, 3)))
plt.plot(x, y, color='r')
plt.errorbar(m, P_mean, yerr=P_std, fmt='.', color='b')

ax2=plt.subplot(212,sharex=ax1)
x_r = np.array([0, 8])
y_r = np.array([0, 0])
H = np.full(len(P_mean), 1)
H_err = np.full(len(P_mean), 1)
for i in range(len(P_mean)):
    H[i] = P_mean[i] - sol[0] * m[i] - sol[2]
    H_err[i] = np.sqrt(P_std[i]**2)
ax2.set_xlabel("m")
ax2.set_ylabel("Residuen [hPa]")
plt.plot(x_r, y_r, color='r')
plt.errorbar(m, H, yerr=H_err, fmt='.', color='b')
plt.show()

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))