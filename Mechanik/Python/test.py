# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:27:45 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

"""
# "Kerbe 1"
data = p.lese_lab_datei("lab/Feder2/Stab_Massen/Aussen-5.lab")
t = data[:,1]
U = data[:,2]
plt.figure(1)
t, U = p.untermenge_daten(t, U, 0, 40)
plt.plot(t, U)
plt.xlabel("t [s]")
plt.ylabel("U [V]")

# "Kerbe 3"
data = p.lese_lab_datei("lab/Feder2/Stab_Massen/Aussen-3.lab")
t = data[:,1]
U = data[:,2]
plt.figure(2)
t, U, = p.untermenge_daten(t, U, 0, 40)
plt.plot(t, U)
plt.xlabel("t [s]")
plt.ylabel("U [V]")
"""


# Feder 3
for i in range(1,6):
    data = p.lese_lab_datei("lab/Feder3/Quadrat/stab{:1d}.lab".format(i))
    t = data[:,1]
    U = data[:,2]
    plt.figure(i)
    plt.plot(t, U)