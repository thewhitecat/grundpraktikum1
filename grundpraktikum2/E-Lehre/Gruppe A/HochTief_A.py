# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:40:06 2017

@author: Tim
"""


import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p


messung1=p.lese_lab_datei('Gruppe A/pass3.lab')
#Index,zeit,Uin,Iin,phi,UA2,UB2,?,f0,f1,z,hoch,tief
f = messung1[:,9]
Uin = messung1[:,2]
Uin_mean = np.mean(Uin)
#offset korrigiert!
U_hoch = messung1[:,5]
U_tief = messung1[:,6]-(messung1[0,6]-Uin_mean)
U_0 = np.mean(Uin)
Uin_std = np.std(Uin)
errs=np.sqrt(Uin_std**2 + (0.0*3)**2)
phase = messung1[:,4]

plt.figure(4)
plt.plot(f[1:-1],phase[1:-1])
plt.xlabel('$f$/Hz')
plt.ylabel('$\phi$/deg')
plt.axhline(45,linestyle='dashed')
plt.show()


plt.figure(0)
plt.errorbar(f,U_tief,yerr=errs)
plt.errorbar(f,U_hoch,yerr=errs)
plt.axhline(U_0/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.ylabel('$U_a$/V')
plt.xlabel('$f$/Hz')
plt.show()





plt.figure(1)
plt.errorbar(f,U_tief*1.01,yerr=errs)
plt.errorbar(f,U_hoch*1.01,yerr=errs)
plt.axhline(U_0/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.title('Systematischer Fehler addiert')
plt.show()

plt.figure(2)
plt.errorbar(f,U_tief*0.99,yerr=errs)
plt.errorbar(f,U_hoch*0.99,yerr=errs)
plt.axhline(U_0/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.title('Systematischer Fehler subtrahiert')
plt.show()





