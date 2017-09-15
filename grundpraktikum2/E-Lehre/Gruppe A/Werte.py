# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 10:30:14 2017

@author: morit
"""

import numpy as np
import Praktikum as p
#Iges Minimum 4,3,2
w0 = np.array([2216.,2216.,2235.])
w0err = np.array([50.,65.,80.])
f_0,sig_f = p.gewichtetes_mittel(w0,w0err)
#f_0 = np.mean(w0)
#sig_f = np.std(w0err)

U0err = [0.005,0.009,0.002]
dw = np.array([737.,488.,738.])
dwerr = np.array([64.,110.,49.])
dwmid,dwstd =  p.gewichtetes_mittel(dw,dwerr)
#dwmid = np.mean(dw)
#dwstd = np.std(dw)
Q = f_0/dwmid
sig = Q * np.sqrt((sig_f/f_0)**2 + (dwstd/dwmid)**2)
print Q, sig

Q2 = w0/dw
sig = Q2 * np.sqrt((w0err/w0)**2 + (dwerr/dw)**2)
print Q2,sig
n = len(sig)
w = 1./(sig)**2
xm = sum(w*Q2)/sum(w)
dext = np.sqrt( ( 1./(n-1)*np.sum(w*(xm-Q2)**2))/sum(w))
dint =  np.sqrt(1./sum(w))
print xm,dext,dint


