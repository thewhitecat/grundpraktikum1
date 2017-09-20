# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:05:47 2017

@author: Tim
"""

import numpy as np
import Praktikum as p
import matplotlib.pyplot as plt

kelvin = 273.15

data_eis = p.lese_lab_datei('Eis.lab')
data_kochen = p.lese_lab_datei('Kochwn.lab')

eis = np.mean(data_eis[:,3])+kelvin
kochen = np.mean(data_kochen[:,3])+kelvin

#T_real = a* T_cassy +b
a = 100.0/(kochen-eis)
b = kelvin-a*eis

raum1 = p.lese_lab_datei('Raum1.lab')[:,3]
raum2 = p.lese_lab_datei('Raum2.lab')[:,3]
raum3 = p.lese_lab_datei('Raum3.lab')[:,3]
raum4 = p.lese_lab_datei('Raum4.lab')[:,3]

r1,r2,r3,r4 = np.mean(raum1),np.mean(raum2),np.mean(raum3),np.mean(raum4)
