# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:29:18 2017

@author: Moritz
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import Kondensator_entladung_neu as k

def merge(list1, list2):
    for i in list2:
        list1.append(i)
    return list1

def linreg(x,y,dy):
    x,y = p.untermenge_daten(x,y,0.0001,0.0015)
    xt,dy = p.untermenge_daten(x,dy,0.0001,0.0015)
    a, ea, b, eb, chiq, cov = p.lineare_regression(x,y,dy)
    return a,ea,b,eb,chiq,x,y,dy

def pictures(t,I=None,U=None,lnI=None,lnU=None,dlnI=None,dlnU=None):
    if I!=None:
        plt.subplots()
        plt.plot(t,I)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[A]")
        plt.title("Rohdaten Strom")
    if U!=None:
        plt.subplots()
        plt.plot(t,U)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Spannung[V]")
        plt.title("Rohdaten Spannung")
    if lnI!=None:
        plt.subplots()
        plt.plot(t,lnI)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(A)]")
        plt.title("log Strom")
    if lnU!=None:
        plt.subplots()
        plt.plot(t,lnU)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(V)]")
        plt.title("log Spannung")
    if dlnI!=None:
        a,ea,b,eb,chiq,x,y,dy = linreg(t,lnI,dlnI)
        plt.subplots()
        plt.errorbar(x,a*x+b,yerr = dy)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(A)]")
        plt.title("Lineare Regression ln(I)")
        plt.figtext(0.7,0.7,
            '\n$\mu=$'+str(np.round(a,2))+'hPa\n'
            +'$\sigma=$'+str(np.round(ea,2))+'hPa\n'
            +'chi^2/f='+str(np.round(chiq/(len(x)-1),2)))
        res = y-(x*a+b)
        plt.subplots()
        plt.plot(x, np.full(len(x),0), color='r')
        plt.xlabel("Zeit[s]")
        plt.ylabel("Residuen")
        plt.title("Residuen ln(I)")
        plt.errorbar(x,res,yerr = dy,fmt='.')
    if dlnU!=None:
        a,ea,b,eb,chiq,x,y,dy = linreg(t,lnU,dlnU)
        plt.subplots()
        plt.errorbar(x,a*x+b,yerr = dy)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(V)]")
        plt.title("Lineare Regression ln(U)")
        plt.figtext(0.7,0.7,
            '\n$\mu=$'+str(np.round(a,2))+'hPa\n'
            +'$\sigma=$'+str(np.round(ea,2))+'hPa\n'
            +'chi^2/f='+str(np.round(chiq/(len(x)-1),2)))
        res = y-(x*a+b)
        plt.subplots()
        plt.plot(x, np.full(len(x),0), color='r')
        plt.xlabel("Zeit[s]")
        plt.ylabel("Residuen")
        plt.title("Residuen ln(U)")
        plt.errorbar(x,res,yerr = dy,fmt='.')
    

data = []
data.append(p.lese_lab_datei('lab/Auf_47_01.lab'))
data.append(p.lese_lab_datei('lab/Auf_47_02.lab'))
data.append(p.lese_lab_datei('lab/Auf_47_03.lab'))
data.append(p.lese_lab_datei('lab/Auf_47_04.lab'))
data.append(p.lese_lab_datei('lab/Auf_47_05.lab'))

Uchiqs = []
UTs = []
UTstat  = []
Ichiqs = []
ITs = []
ITstat  = []

R = 98.76
dR = 0.06
dRsys = 2.2

for i in range(len(data)):
    array = data[i]
    t = array[:,1]

    I = -array[:,2]-0.0004#offset
    dI = 0.00045
    I = np.absolute(I)
    logI = log(I)
    dlogI = dI/I
    
    U = array[:,3]
    dU = 0.045
    U0 = array[500:,3]
    mU0,dU0 = np.mean(U0),np.std(U0,ddof=1)
    Udiff = np.absolute((mU0-U))
    logU = log(Udiff)
    dlogU = dU/U
    
    a,ea,b,eb,chiq,x,y,dy = linreg(t,logU,dlogU)
    
    Uchiqs.append(chiq/(len(x)-1))
    UTs.append(-1/a)
    UTstat.append(ea/(a**2))
    
    a,ea,b,eb,chiq,x,y,dy = linreg(t,logI,dlogI)
    
    Ichiqs.append(chiq/(len(x)-1))
    ITs.append(-1/a)
    ITstat.append(ea/(a**2))
    if i==0:
        pictures(t,lnI=logI,lnU=logU,dlnI=dlogI,dlnU=dlogU)

Tend,Tendstat = k.alles()
Ts = merge(UTs,ITs)
Ts = merge(Ts,Tend)
Tstat = merge(UTstat,ITstat)
Tstat = merge(Tstat,Tendstat)
Tstat = np.array(Tstat)
Tmu,Terr = p.gewichtetes_mittel(Ts,Tstat)
C = Tmu/R
Cerr = np.sqrt((Terr/R)**2+(Tmu*dR/R**2)**2)
Csys = (Tmu*dRsys/R**2)
print C,Cerr,Csys
Cerrall = np.sqrt(Cerr**2+Csys**2)
Cgesamt, Cgesamtstat = p.gewichtetes_mittel(np.array([C,4.88*10**(-6)]),np.array([Cerr,0.0122*10**(-6)]))
print Cgesamt, Cgesamtstat
