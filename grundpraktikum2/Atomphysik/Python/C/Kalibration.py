# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:26:03 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt
import timeit
import auswertung_nur_Methoden as AM

start_time=timeit.default_timer()

Kel = 273.15

data_eis = p.lese_lab_datei("eiswasser.lab")
data_koch = p.lese_lab_datei("kochendwasser.lab")

temp_eis = Kel + data_eis[:,3]
temp_koch = Kel + data_koch[:,3]

NP = np.mean(temp_eis)
NP_std = np.std(temp_eis)
SP = np.mean(temp_koch)
SP_std = np.std(temp_koch)

k = (100-0)/(SP-NP)
sig_k = k * np.sqrt(((NP_std + SP_std)/(SP - NP))**2)
off = 0 - k * NP
sig_off = np.sqrt((k * NP_std)**2 + (NP * sig_k)**2)

def temp(T_gem):
    T_real = k * T_gem + off + Kel
    return T_real

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))