# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 17:12:27 2017

@author: morit
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

m = np.array([5.1,4.8,5.0,4.9,4.7,5.1,5.0,4.8])
mean = np.mean(m)#Korrektur von +1.2 zu Literaturwert
std = np.std(m,ddof =1)
lam = 522.66e-9
lamerr = np.sqrt(2.03e-9**2 + 1.92e-9**2)
lamstat = 2.03e-9
lamsys = 1.92e-9
L = 0.01
dL = 0.0001#8°

dn = mean *lam/(2.*L)

dnstat = np.sqrt((lam/(2.*L)*std)**2)
dnsys = np.sqrt((mean/(2*L) * lamerr)**2 + (dn/L * dL)**2)

print "dn: ", dn, dnstat,dnsys

nl = 1+2.6108675e-7*979.
nlerr = 979.*np.sqrt((2.77e-9)**2 + (1.40e-9)**2)
print "nLuft:",nl, nlerr
n = nl + dn
nstat = np.sqrt(dnstat**2)
nsys = np.sqrt(dnsys**2+nlerr**2)
print "ergebnis:", n-1, nstat,nsys

nlit = 4.16e-4/1013*979
sigmas = abs(n-1-nlit)/np.sqrt(nstat**2 + nsys**2)
print sigmas
rel = abs((n-1)/(nlit)*100 - 100)
relsig = np.sqrt(nstat**2 + nsys**2)/(n-1)