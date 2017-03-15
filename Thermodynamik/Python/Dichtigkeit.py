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
import Rauschmessung as Rm

start_time=timeit.default_timer()

#Lese alle Datensätze ein
M_S_1 = p.lese_lab_datei('lab/Dichtigkeitsmessung_vorher.lab')
p_v = M_S_1[:, 4]
t_v = M_S_1[:, 2]

M_S_2 = p.lese_lab_datei('lab/Dichtigkeitsmessung_nachher_2.lab')
p_n = M_S_2[:, 4]
t_n = M_S_1[:, 2]

#
def func(t, p):
    a, var, c = Rm(p)
    p_err = np.full(p.size(), var)
    rate, rate_var, b, eb, chiq, corr = p.lineare_regression(t, p, p_err)
    return rate, rate_var, b, eb, chiq

leckrate_v, Fehler_v = func(t_v, p_v)
leckrate_n, Fehler_n = func(t_n, p_n)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))