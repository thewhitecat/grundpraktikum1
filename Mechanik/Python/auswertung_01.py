# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:00:06 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

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

def get_peaks(x, y):
    zeros = get_zeros(x, y, index_output=False)
    peaks = []
    index = []
    
    for n in range(len(zeros)-1):
        peaks.append(p.peak(x, y, zeros[n][0], zeros[n+1][0]))
    for peak in peaks:
        indx = find_nearest(x, peak)
        if (np.abs(y[indx]) > 0.05*np.mean(np.absolute(y[0:5]))):
            index.append(indx)
    index = np.array(index)
    
    return index




def stab_mitte(feder=2):
    for i in range(5):
        data = p.lese_lab_datei("lab/Feder {:1d}/Stab_mitte/messung{:1d}.lab".format(feder, i+1))
        t = data[:,1]
        U = data[:,2]



