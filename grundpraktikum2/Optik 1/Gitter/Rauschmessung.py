# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 14:10:50 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit

start_time=timeit.default_timer()

data_raw = np.genfromtxt('Rauschen_Nullte_Ordnung.txt', delimiter = ',', skip_header = 2);
                    
def degtorad(deg):
    data = []
    for i in range(len(deg)):
        rad = (deg[i][0] + deg[i][1]/60) * 2 * np.pi / 360 
        data += [rad]
    return data

def mintodeg(deg):
    data = []
    for i in range(len(deg)):
        grad = deg[i][0] + deg[i][1]/60
        data += [grad]
    return data

data = degtorad(data_raw)
data_grad = mintodeg(data_raw)

bins_grad = np.arange(84.0,85.0, 1./60)
#plt.figure(2)
plt.hist(data_grad,bins=bins_grad)
plt.xlabel('Winkel [Grad]')
#plt.xlim(-0.04,0.0)
plt.ylabel('#')
plt.title('Rauschmessung Winkel')

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))