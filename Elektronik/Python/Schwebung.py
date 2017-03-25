# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 09:49:39 2017

@author: grldm
"""

import Praktikum as prak
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt

start_time=timeit.default_timer()

data = []
data.append(prak.lese_lab_datei('lab/Koppel_mitAbstand_1.lab'))
data.append(prak.lese_lab_datei('lab/Koppel_mitAbstand_2.lab'))
#data.append(prak.lese_lab_datei('lab/Koppel_03.lab'))
#data.append(prak.lese_lab_datei('lab/Koppel_04.lab'))
#data.append(prak.lese_lab_datei('lab/Koppel_05.lab'))

f_1_1 = []
f_1_2 = []
f_2_1 = []
f_2_2 = []
for i in range(len(data)):
    #i +=3
    dat = data[i]
    t = dat[:,1]
    U1 = dat[:,2]
    U2 = dat[:,3]
    freq,amp = prak.fourier_fft(t,U1)
    #fourier
    F_1, U_1 = prak.fourier_fft(t, U1)
    F_2, U_2 = prak.fourier_fft(t, U2)

    #finde peaks
    peak1_1 = prak.peak(F_1, U_1, 600, 750)
    peak1_2 = prak.peak(F_1, U_1, 750, 900)
    peak2_1 = prak.peak(F_2, U_2, 600, 750)
    peak2_2 = prak.peak(F_2, U_2, 750, 900)
    f_1_1.append(peak1_1)
    f_1_2.append(peak1_2)
    f_2_1.append(peak2_1)
    f_2_2.append(peak2_2)

#mittelwert und Fehler auf Frequenzen
mw_f_1 = 282.4#np.mean(f_1_1)
mw_f_2 = 486.9#np.mean(f_2_1)
std_f_1 = 0.4#np.std(f_1_1)
std_f_2 = 0.4#np.std(f_2_1)

#bestimme k und Fehler auf k
k = (mw_f_2**2 - mw_f_1**2)/(mw_f_1**2 + mw_f_2**2)
zahl=(mw_f_1**2 - mw_f_2**2)
nenn=(mw_f_2**2 + mw_f_1**2)
dk = np.sqrt(((1/nenn - zahl/nenn**2)*2*mw_f_1*std_f_1)**2 + ((-1/nenn - zahl/nenn**2)*2*mw_f_2*std_f_1)**2)

#bestimme Erwartung für delta_t und Fehler auf delta_t
L = 0.009
R = 2.8
C = 4.9 * 10**(-6)
dL = 0.0025 * L
dR = 0.0025 * R
dC = 6 * 10**(-9)
f_s = (mw_f_2 - mw_f_1)/2
dt_dk = -1/(2*np.pi*f_s) * (1/R * np.sqrt(L/C))/(1 + (k/R * np.sqrt(L/C))**2)
dt_dR = 1/(2*np.pi*f_s) * (k/R**2 * np.sqrt(L/C))/(1 + (k/R * np.sqrt(L/C))**2)
dt_dC = 1/(4*np.pi*f_s) * (k/R * np.sqrt(L) * C**(-3/2))/(1 + (k/R * np.sqrt(L/C))**2)
dt_dL = -1/(4*np.pi*f_s) * (k/R * np.sqrt(1/(C*L)))/(1 + (k/R * np.sqrt(L/C))**2)
del_t = 1/(2 * np.pi * f_s) * (np.pi/2 - np.arctan(k/R * np.sqrt(L/C)))
d_del_t = np.sqrt((dt_dk * dk)**2 + (dt_dL * dL)**2 + (dt_dC * dC)**2 + (dt_dR * dR)**2)

#bestimme delta_t und Fehler auf delta_t aus Daten
def get_zeros(t,U,index_output=True):
    '''
    gibt liste mit Tupeln der Form (index, index+1) zurück,
    dieser index und nächster sind die "nullstellen"
    '''
    zeros=[]
    for i in range(len(U)-1):
        if U[i]>0 and U[i+1]<0:
            zeros.append((t[i],U[i],i))
        elif U[i]<0 and U[i+1]>0:
            zeros.append((t[i],U[i],i))
        elif U[i]==0 and U[i-1] and i>0:
            zeros.append((t[i],U[i],i))
    #don't bother with this stuff
    if index_output==False:
        return zeros
    else:
        index=[]
        for x in zeros:
            index.append(x[2])
        return index

def get_extrema(x, y, zeros):
    extrema = []
    for i in range(len(zeros)-1):
        extremum = prak.peak(x, np.absolute(y), x[zeros[i]], x[zeros[i+1]])
        extrema.append(extremum)
    return extrema

dt = []
for i in range(len(data)):
    #i +=3
    dat = data[i]
    t = dat[:,1]
    U1 = dat[:,2]
    U2 = dat[:,3]
    #suche Nullstellen und Extrema in beiden Spannungsverläufen
    zero_U1 = get_zeros(t[:2500], U1[:2500])
    zero_U2 = get_zeros(t[:2500], U2[:2500])
    extrema_U1 = get_extrema(t, U1, zero_U1)
    extrema_U2 = get_extrema(t, U2, zero_U2)
    zeros_U1 = []
    zeros_U2 = []
    extremas_U1 = []
    extremas_U2 = []
    n = min(len(zero_U1), len(zero_U2), len(extrema_U1), len(extrema_U2))
    for i in range(n):
        zeros_U1.append(t[zero_U1[i]])
        zeros_U2.append(t[zero_U2[i]])
        extremas_U1.append(extrema_U1[i])
        extremas_U2.append(extrema_U2[i])
    dt = []
    for i in range(n):
        dt_1 = zeros_U1[i] - extremas_U2[i]
        dt_2 = zeros_U2[i] - extremas_U1[i]
        dt.append(dt_1)
        dt.append(dt_2)

dt_end = np.mean(dt)
std_dt_end = np.std(dt)

print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))