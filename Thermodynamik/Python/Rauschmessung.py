# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:06:56 2017

@author: Ben
"""

import Praktikum as p
import matplotlib.pyplot as plt
import math
import numpy as np

data = p.lese_lab_datei('lab/Rauschmessungen.lab')
T = data[:,2]
p = data[:,4]

#Gibt aus:
#Mittelwert, Standardabweichung, Ferhler auf Mittelwert
def mean(data):
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