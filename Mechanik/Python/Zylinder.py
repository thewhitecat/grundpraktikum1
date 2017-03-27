# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:31:26 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

data = []
data.append(p.lese_lab_datei('lab/Feder3/teller/teller1.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller2.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller3.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller4.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller5.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller6.lab'))
data.append(p.lese_lab_datei('lab/Feder3/teller/teller7.lab'))
for data in data:
    t = data[:,1]
    U = data[:,2]
    freq,amp = p.fourier_fft(t,U)