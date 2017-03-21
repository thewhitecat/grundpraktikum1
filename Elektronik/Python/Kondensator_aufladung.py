# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:49:42 2017

@author: Ben
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

data = p.lese_lab_datei('lab/Auf_47_01.lab')

t = data[:,1]

I = -data[:,2]
dI = 0.00045
I0 = data[500:,2]
mI0,dI0 = np.mean(I0),np.std(I0,ddof=1)
logI = log(I)
dlogI = dI/I


U = data[:,3]
dU = 0.047
U0 = data[500:,3]
mU0,dU0 = np.mean(U0),np.std(U0,ddof=1)
logU = log((mU0-U))
dlogU = dU/U

R = 99
dR = 2.1

def linreg(x,y,dy):
    x,y = p.untermenge_daten(x,y,0,0.002)
    xt,dy = p.untermenge_daten(x,dy,0,0.002)
    a, ea, b, eb, chiq, cov = p.lineare_regression(x,y,dy)
    return a,ea,chiq,x,y,dy
    

def plots(rohdaten,logs,linrege):
    if rohdaten==1:
        plt.subplots()
        plt.plot(t,I)
        plt.subplots()
        plt.plot(t,U)
    if logs==1:
        plt.subplots()
        plt.plot(t,logI)
        plt.subplots()
        plt.plot(t,logU)
    if linrege==1:
        a,ea,chiq,x,y,dy = linreg(t,logU,dlogU)
        plt.subplots()
        plt.errorbar(x,a*x+b,yerr = dy)
        res = y-(x*a+b)
        plt.subplots()
        plt.plot(x, np.full(len(x),0), color='r')
        plt.errorbar(x,res,yerr = dy,fmt='.')
        
        linreg(t,logI,dlogI)
        plt.subplots()
        plt.errorbar(x,a*x+b,yerr = dy)
        res = y-(x*a+b)
        plt.subplots()
        plt.plot(x, np.full(len(x),0), color='r')
        plt.errorbar(x,res,yerr = dy,fmt='.')
        
def alles():
    data = []
    Uchiqs = []
    UTs = []
    UTstat  = []
    
    Ichiqs = []
    ITs = []
    ITstat  = []
    data.append(p.lese_lab_datei('lab/Auf_47_01.lab'))
    data.append(p.lese_lab_datei('lab/Auf_47_02.lab'))
    data.append(p.lese_lab_datei('lab/Auf_47_03.lab'))
    data.append(p.lese_lab_datei('lab/Auf_47_04.lab'))
    data.append(p.lese_lab_datei('lab/Auf_47_05.lab'))
    for i in range(len(data)):
        array = data[i]
        t = array[:,1]
    
        I = -array[:,2]
        dI = 0.00045
        logI = log(I)
        dlogI = dI/I
        
        R = 99
        dR = 2.1
        
        U = array[:,3]
        dU = 0.047
        U0 = array[500:,3]
        mU0,dU0 = np.mean(U0),np.std(U0,ddof=1)
        logU = log((mU0-U))
        dlogU = dU/U
        
        a,ea,chiq,x,y,dy = linreg(t,logU,dlogU)
        
        Uchiqs.append(chiq/len(x))
        UTs.append(-1/a)
        UTstat.append(ea/(a**2))
        
        a,ea,chiq,x,y,dy = linreg(t,logI,dlogI)
        
        Ichiqs.append(chiq/len(x))
        ITs.append(-1/a)
        ITstat.append(ea/(a**2))
    Ts = merge(UTs,ITs)
    
    Tstat = np.array(merge(UTstat,ITstat))
    Tmu,Terr = p.gewichtetes_mittel(Ts,Tstat)
    C = Tmu/R
    Cerr = np.sqrt((Terr/R)**2+(Tmu*dR/R**2)**2)
    print C,Cerr
        
def merge(list1, list2):
    for i in list2:
        list1.append(i)
    return list1
alles()