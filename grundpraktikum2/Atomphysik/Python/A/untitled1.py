# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:20:04 2017

@author: morit
"""
import Histogramme as h
import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt

def func(x,a,b,c):
    return a+b*(x**(c))

def anpassung(T, U,sigT):
    plt.plot(T,U)
    popt,pcov = opt.curve_fit(func,T,U,sigma=sigT,absolute_sigma=True,p0[])
    xwerte = np.linspace(T[0],T[-1],1000)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)
    print popt







def main():
    messing = h.get_werte('weiss')
    T = messing[0]
    Terr = messing[3]
    U = messing[2]
    anpassung(T,U,Terr)
    






if __name__ == "__main__":
    main()