# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:05:49 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt

start_time=timeit.default_timer()

#Lese alle Datensätze ein
M_S_1 = p.lese_lab_datei('Lab/Temperatur_Eiswasser.lab')
T_E = M_S_1[:, 2]

M_S_2 = p.lese_lab_datei('Lab/Temperatur_siedend.lab')
T_S = M_S_2[:, 2]

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))