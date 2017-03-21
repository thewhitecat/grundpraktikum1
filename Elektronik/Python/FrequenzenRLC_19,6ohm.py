# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:44:48 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

#messung einlesen
messung1=p.lese_lab_datei('lab/19,6Ohm/messung1.lab')
messung2=p.lese_lab_datei('lab/19,6Ohm/messung2.lab')
messung3=p.lese_lab_datei('lab/19,6Ohm/messung3.lab')
messung4=p.lese_lab_datei('lab/19,6Ohm/messung4.lab')
messung5=p.lese_lab_datei('lab/19,6Ohm/messung5.lab')

messungen=[messung1,messung2,messung3,messung4,messung5]
#messung 1 für testzwecke
t1=messung1[:,1]
U1=messung1[:,3]

t4,U4=messung4[:,1],messung4[:,3]
t5,U5=messung5[:,1],messung5[:,3]

#methode zur bestimmung der frequenzen
def get_freq(messung):
    t=messung[:,1]
    U=messung[:,3]
    
    freq,amp=p.fourier_fft(t,U)
    peak=p.peakfinder_schwerpunkt(freq,amp)
    return peak

#peak mittelwerte und fehler und fehler auf mittelwert.
def f_fourier(messungen):
    peaks=[]
    for x in messungen:
        peaks.append(get_freq(x))
    
    mean,std=np.mean(peaks),np.std(peaks,ddof=1)
    mean_error=std/np.sqrt(len(peaks))
    
    return mean,std,mean_error

#ab hier versuch durch abzählen...
#erste nullstelle suchen -> dann n nullstellen abzählen -> dann zeit nehmen
def get_zeros(t,U,index_output=True):
    '''
    gibt liste mit Tupeln der Form (t,U,index) zurück,
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
            index.append((x[2],x[2]+1))
        return index

#wrapper abzähler
#annahme: gleichverteilungsfehler beim abzählen
def f_count(t,U):
    index=get_zeros(t,U)
    times=[]
    error_times=[]
    periods=[]
    error_periods=[]
    
    for x in index:
        times.append((t[x[1]]+t[x[0]])/2)
        error_times.append((t[x[1]]-t[x[0]])/np.sqrt(12))
    
    for i in range(len(times)-1):
        periods.append(2*(times[i+1]-times[i]))
        error_periods.append(np.sqrt(error_times[i+1]**2+error_times[i]**2))
    periods=periods[:-1]
    error_periods=error_periods[:-1]
    output=p.gewichtetes_mittel(np.array(periods),np.array(error_periods))
    return(1/output[0],output[1]/output[0]**2)
    return output



def wrapper_f_count(messungen):
    f,sigma_f=[],[]
    for x in messungen:
        f.append(f_count(x[:,1],x[:,3])[0])
        sigma_f.append(f_count(x[:,1],x[:,3])[1])
    
    output=p.gewichtetes_mittel(np.array(f),np.array(sigma_f))
    return output

'''
#debug
debug4=f_count(t4,U4)
plt.plot(t4,U4)
plt.axhline(0)
for x in debug4:
    plt.axvline(x)   
'''






