# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:06:56 2017

@author: Ben
"""

import Praktikum as p
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.constants as const
import math
import numpy as np

data = p.lese_lab_datei('lab/Rauschmessungen.lab')
data2 = p.lese_lab_datei('lab/Temperatur_Eiswasser.lab')
T = data2[:,2]
p = data[:,4]

def mean(data):
    '''
    Eingabe: Eindimensionales Array mit Einzelmessungen
    Gibt aus:
    Mittelwert, Standardabweichung, Ferhler auf Mittelwert
    '''
    mean = 0
    N = len(data)
    for i in range(N):
        mean += data[i]
    mean = mean/N
    summe = 0
    N = len(data)
    for i in range(N):
        summe += (data[i]-mean)**2
    var = math.sqrt((1.0/(N-1))*summe)
    fehler = var/math.sqrt(N)
    return mean,var,fehler

Tm,Tstd,Tf = mean(T)
print "Temperatur:",Tm," Fehler:", Tstd
pm,pstd,pf = mean(p)
print "Druck:",pm," Fehler:", pstd

def histogramm(data,title,xlabel):
    ax = plt.subplot(1,1,1)
    plt.ylabel("#")
    plt.xlabel("xlabel")
    mu,sigma,f = mean(data)
    norm = np.full(data.size,1.0/data.size)
    n,bins,patches = ax.hist(data,weights=norm,rwidth=2)
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, 'r--', linewidth=2)
    
histogramm(T,"test","teset")