# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 14:10:50 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

data_raw = np.genfromtxt('Rauschen_Nullte_Ordnung.txt', delimiter = ',', skip_header = 2);
                
data = AM.degtorad(data_raw)
data_grad = AM.mintodeg(data_raw)

Fehler_Winkel = np.std(data)
Winkel_Nullte_Ordnung = np.mean(data)

print("Winkel der Nullten Ordnung: ", Winkel_Nullte_Ordnung)
print("Fehler: ", Fehler_Winkel)

bins_grad = np.arange(84.0,85.0, 1./60)
#plt.figure(2)
plt.hist(data_grad,bins=bins_grad)
plt.xlabel('Winkel [Grad]')
#plt.xlim(-0.04,0.0)
plt.ylabel('#')
plt.title('Rauschmessung Winkel')

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))