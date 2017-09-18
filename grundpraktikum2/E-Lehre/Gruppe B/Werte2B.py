# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 10:30:14 2017

@author: morit
"""

import numpy as np
import Praktikum as p
#####################################
#Iges Minimum 4,3,2
w0 = np.array([2272.,2285.])
w0err = np.array([54.,55.])
f_0,sig_f = p.gewichtetes_mittel(w0,w0err)
U0 = [0.065,0.063]
U0err = [0.010,0.010]
dw = np.array([750.,700.])
dwerr = np.array([81.,79.])
dwsys = np.array([24.,23.])
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
sys = Q2 * np.sqrt((0/w0)**2 + (dwsys/dw)**2)
print Q2,sig,sys
sig = np.sqrt(sig**2+sys**2)
n = len(sig)
w = 1./(sig)**2
xm = sum(w*Q2)/sum(w)
dext = np.sqrt( ( 1./(n-1)*np.sum(w*(xm-Q2)**2))/sum(w))
dint =  np.sqrt(1./sum(w))
print gew_mittelwert(w0,w0err)
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
print gew_mittelwert(w0,w0err)
print Q,Qerr
print gew_mittelwert(Q,Qerr)
print "######"

####################################

phi0 = np.array([2094,2094])
phierr = np.array([16,16])
print gew_mittelwert(phi0,phierr)
print "######"

####################################

w0 = np.array([2275,2275])
w0err = np.array([30,30])
N = np.array([71,70])
Nerr = np.array([9,9])
print gew_mittelwert(w0,w0err)
print gew_mittelwert(N,Nerr)