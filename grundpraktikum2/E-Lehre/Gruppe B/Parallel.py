# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:29:28 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum


data = Praktikum.lese_lab_datei('lab/Parallell_unendlich2.lab')

f = data[:,-2]
phi = data[:,-7]
I = data[:,3]
Z = data[:,-1]
IC = data[:,-3]
IL = data[:,-6]


plt.figure(0)
ax1 = plt.subplot(111)
plt.plot(f,I,label='I')
plt.ylabel('I/A')
plt.xlabel('f/Hz')

ax2 = ax1.twinx()
plt.plot(f,Z,color = 'r',label='Z')
plt.ylabel('Z/$\Omega$')

plt.show()

plt.figure(1)
plt.plot(f,phi,marker='.')
plt.ylabel('$\phi$/deg')
plt.xlabel('f/Hz')
plt.axhline(0)
plt.show()

plt.figure()
plt.plot(f,IC)
plt.plot(f,IL)
plt.plot(f,I)
plt.show()


