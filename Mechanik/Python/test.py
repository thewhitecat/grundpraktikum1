# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:27:45 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt


data = p.lese_lab_datei("lab/Feder2/Stab_Massen/Aussen-3.lab")
t = data[:,1]
U = data[:,2]
plt.figure(1)
plt.plot(t, U)