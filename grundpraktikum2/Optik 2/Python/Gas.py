# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 17:12:27 2017

@author: morit
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

m = [5.1,4.8,5.0,4.9,4.7,5.1,5.0,4.8]
mean = np.mean(m)
std = np.std(m)
lam = 522.66e-9
lamstat = 2.03e-9
lamsys = 1.92e-9
L = 0.01

dn = mean *lam/(2*L)

dnerr = np.sqrt((lam/(2*L)*std)**2 + (mean/(2*L) * lamstat)**2)

print dn, dnerr

nl = 1+2.6108675e-7*979.
nlerr = 979*np.sqrt((3.4805e-9)**2 + (9.639e-10)**2)
print nl
n = nl +dn
nerr = np.sqrt(dnerr**2+nlerr**2)
print n-1, nerr