# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:36:45 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum

R = 9.988
C = 4.475e-6

data = Praktikum.lese_lab_datei('lab/Hoch-Tief.lab')

U_1 = data[:,2]
U_0,rauschen = np.mean(U_1), np.std(U_1,ddof = 1)


f = data[:,-2]

#offset von vormessen
U_tief = data[:,-3]+0.0045
U_hoch = data[:,-6]+0.01


tief,hoch = U_tief/U_0,U_hoch/U_0
errs = np.full(len(tief),rauschen/U_0)

plt.figure()
plt.errorbar(f,tief,yerr=errs,marker = '.')
plt.errorbar(f,hoch,yerr=errs,marker = '.')
plt.axhline(1, color = 'red')
plt.axhline(1/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.ylabel('$U_a/U_e$')
plt.xlabel('$f$/Hz')

x=np.linspace(0.00001,8000,10000)
#plt.plot(x,U_0/np.sqrt((1/(x*2*np.pi*R*C))**2+1))
#plt.plot(x,U_0/np.sqrt(1+(x*2*np.pi*C*R)**2))


