# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 18:46:50 2017

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

#Rauschmessung in Spannung
U1 = U[:4000]
bins_U = np.arange(1.8,2.2, 0.0015)
plt.figure(1)
plt.hist(U1,bins=bins_U)
plt.xlabel('Spannung [V]')
plt.xlim(1.9, 2.3)
plt.ylabel('#')
plt.title('Rauschmessung Spannung')

#Rauschmessung in Strom
I1 = I[:4000]
bins_I = np.arange(-0.04,0.0, 0.00015)
plt.figure(2)
plt.hist(I1,bins=bins_I)
plt.xlabel('Strom [A]')
plt.xlim(-0.04,0.0)
plt.ylabel('#')
plt.title('Rauschmessung Strom')

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))