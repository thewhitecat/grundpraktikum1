# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 10:30:14 2017

@author: morit
"""

import numpy as np
import Praktikum as p
#####################################
#Iges Minimum 4,3,2
w0 = np.array([2216.,2216.,2235.])
w0err = np.array([50.,65.,80.])
f_0,sig_f = p.gewichtetes_mittel(w0,w0err)
#f_0 = np.mean(w0)
#sig_f = np.std(w0err)
U0 = []
U0err = [0.005,0.009,0.002]
dw = np.array([737.,488.,738.])
dwerr = np.array([64.,110.,49.])
dwmid,dwstd =  p.gewichtetes_mittel(dw,dwerr)
#dwmid = np.mean(dw)
#dwstd = np.std(dw)
Q = f_0/dwmid
sig = Q * np.sqrt((sig_f/f_0)**2 + (dwstd/dwmid)**2)
print Q, sig

def gew_mittelwert(Q2, sig):
    n = len(sig)
    w = 1./(sig)**2
    xm = sum(w*Q2)/sum(w)
    dext = np.sqrt( ( 1./(n-1)*np.sum(w*(xm-Q2)**2))/sum(w))
    dint =  np.sqrt(1./sum(w))
    return xm,dext,dint

Q2 = w0/dw
sig = Q2 * np.sqrt((w0err/w0)**2 + (dwerr/dw)**2)
print Q2,sig
n = len(sig)
w = 1./(sig)**2
xm = sum(w*Q2)/sum(w)
dext = np.sqrt( ( 1./(n-1)*np.sum(w*(xm-Q2)**2))/sum(w))
dint =  np.sqrt(1./sum(w))
print xm,dext,dint

#####################################

w0 = np.array([2094.2,2096.1,2093.4])
w0err = np.array([49.2,56.5,51.3])
UL = np.array([0.0850,0.1278,0.1274])
dU = np.array([0.0009,0.0021,0.0017])
U0 = np.array([0.0256,0.0234,0.0390])
U0err = [0.0008,0.0021,0.0017]
Q = UL/U0
Qerr = Q * np.sqrt((dU/UL)**2+ (U0err/U0)**2)
print Q,Qerr
print gew_mittelwert(Q,Qerr)

####################################

phi0 = np.array([2154,2137,2137])
phierr = np.array([42,30,32])
print gew_mittelwert(phi0,phierr)