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
w0err = np.array([23.,29.,17.])
f_0,sig_f = p.gewichtetes_mittel(w0,w0err)
U0 = []
U0err = [0.005,0.009,0.002]
dw = np.array([737.,488.,738.])
dwerr = np.array([19.,43.,24.])
dwmid,dwstd =  p.gewichtetes_mittel(dw,dwerr)

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
print "######"

#####################################

w0 = np.array([2094.6,2095.6,2093.7])
w0err = np.array([33.7,38.2,35.2])/np.sqrt(3)
UL = np.array([0.0850,0.1278,0.1274])
dU = np.array([0.0009,0.0021,0.0017])/np.sqrt(3)
U0 = np.array([0.0256,0.0234,0.0390])
U0err = [0.0008,0.0021,0.0017]/np.sqrt(3)
Q = UL/U0
Qerr = Q * np.sqrt((dU/UL)**2+ (U0err/U0)**2)
print Q,Qerr
print gew_mittelwert(Q,Qerr)
print "######"

####################################

phi0 = np.array([2154,2137,2137])
phierr = np.array([42,30,32])
print gew_mittelwert(phi0,phierr)
print "######"

####################################

w0 = np.array([2218,2216,2219])
w0err = np.array([80,80,80])
N = np.array([55,114,47])
Nerr = np.array([10,99,14])