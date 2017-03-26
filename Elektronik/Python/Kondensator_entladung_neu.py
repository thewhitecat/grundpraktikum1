# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:29:18 2017

@author: Moritz
"""

import Praktikum as p
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

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
        plt.axvline(x=0.0015,color='g')
        plt.axvline(x=0.0001,color='g')
    if lnU!=None:
        plt.subplots()
        plt.plot(t,lnU)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(V)]")
        plt.title("log Spannung")
        
        plt.axvline(x=0.0015,color='g')
        plt.axvline(x=0.0001,color='g')
    if dlnI!=None:
        a,ea,b,eb,chiq,x,y,dy = linreg(t,lnI,dlnI)
        plt.subplots()
        plt.errorbar(x,a*x+b,yerr = dy)
        plt.xlabel("Zeit[s]")
        plt.ylabel("Strom[ln(A)]")
        plt.title("Lineare Regression ln(I)")
        plt.figtext(0.6,0.7,
            '\n$\mu_{Steigung}=$'+str(np.round(a,2))+'\n'
            +'$\sigma_{Steigung}=$'+str(np.round(ea,2))+'\n'
            +'chi^2/f='+str(np.round(chiq/len(x),2)))
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
        plt.figtext(0.6,0.7,
            '\n$\mu_{Steigung}=$'+str(np.round(a,2))+'\n'
            +'$\sigma_{Steigung}=$'+str(np.round(ea,2))+'\n'
            +'chi^2/f='+str(np.round(chiq/len(x),2)))
        res = y-(x*a+b)
        plt.subplots()
        plt.plot(x, np.full(len(x),0), color='r')
        plt.xlabel("Zeit[s]")
        plt.ylabel("Residuen")
        plt.title("Residuen ln(U)")
        plt.errorbar(x,res,yerr = dy,fmt='.')
        
def alles():
    data = []
    data.append(p.lese_lab_datei('lab/Ent_47_01.lab'))
    data.append(p.lese_lab_datei('lab/Ent_47_02.lab'))
    data.append(p.lese_lab_datei('lab/Ent_47_03.lab'))
    data.append(p.lese_lab_datei('lab/Ent_47_04.lab'))
    data.append(p.lese_lab_datei('lab/Ent_47_05.lab'))
    
    Uchiqs = []
    Ua = []
    Ia = []
    Uastd = []
    Iastd = []
    UTs = []
    UTstat  = []
    Ichiqs = []
    ITs = []
    ITstat  = []
    
    R = 98.74
    dR = 0.06
    dRsys = 2.2
    
    for i in range(len(data)):
        array = data[i]
        t = array[:,1]
    
        I = -array[:,2]-0.0004#offset
        U0 = array[500:,2]
        mU0,dU0 = np.mean(U0),np.std(U0,ddof=1)
        dI = dU0
        I = np.absolute(I)
        logI = log(I)
        dlogI = dI/I
        
        U = array[:,3]-0.005
        dU = 0.047
        U0 = array[500:,3]
        mU0,dU0 = np.mean(U0),np.std(U0,ddof=1)
        dU = dU0
        Udiff = np.absolute(U)
        logU = log(Udiff)
        dlogU = dU/U
        
        a,ea,b,eb,chiq,x,y,dy = linreg(t,logU,dlogU)
        
        Uchiqs.append(chiq/len(x))
        UTs.append(-1/a)
        UTstat.append(ea/(a**2))
        Ua.append(a)
        Uastd.append(ea)
        
        a,ea,b,eb,chiq,x,y,dy = linreg(t,logI,dlogI)
        
        Ichiqs.append(chiq/len(x))
        ITs.append(-1/a)
        ITstat.append(ea/(a**2))
        Ia.append(a)
        Iastd.append(ea)
        
        if i==10:
            pictures(t,lnI=logI,lnU=logU,dlnI=dlogI,dlnU=dlogU)
    
    #mittelTU,stdTU = p.gewichtetes_mittel(UTs,np.array(UTstat))
    #mittelTI,stdTI = p.gewichtetes_mittel(ITs,np.array(ITstat))
    mittelUa,stdUa = np.mean(Ua),np.std(Ua,ddof=1)/(len(Ua)-2)
    mittelIa,stdIa = np.mean(Ia),np.std(Ia,ddof=1)/(len(Ia)-2)
#    print mittelUa,stdUa
#    print mittelIa,stdIa
    TU = -1/mittelUa
    TI = -1/mittelIa
    TUstd = stdUa/mittelUa**2
    TIstd = stdIa/mittelIa**2
#    print TU,TUstd
#    print TI,TIstd
    
    return TU,TUstd,TI,TIstd
alles()
