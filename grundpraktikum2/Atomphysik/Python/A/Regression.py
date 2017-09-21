# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:43:13 2017

@author: Tim
"""

import numpy as np
import Histogramme as h
import matplotlib.pyplot as plt
import Praktikum as p

kelvin = 273.15
a, b = 1.0107638757247093, -3.3550993800564015
T0 = (23.70487017571428+kelvin)*a+b

weis = h.get_werte('weiss')
messing = h.get_werte('messing')
schwarz = h.get_werte('schwarz')
spiegel = h.get_werte('spiegel')


def Auswertung(data,i=0,plots = True):
    #kalib anwenden
    T, eT = a*(data[0]+kelvin)+b, data[1]*a+b
    U, eU = data[2], data[3]
    #transformieren und verschieben
    T4, eT4 = T**4-T0**4, 4*T**3*eT
    
    #hier anpassung
    m,em,q,eq,chiq,cov = p.lineare_regression_xy(T4,U,eT4,eU)
    chiq_ndof = chiq/(len(U)-2)
    x_axis = np.linspace(T4[0],T4[-1],100)
    
    if plots == False:
        return m,em,q,eq
    else:
        #hier plot
        plt.figure(i)
    
        ax1 = plt.subplot(211)
        plt.errorbar(T4,U,xerr=eT4,yerr=eU,linestyle='None')
        plt.plot(x_axis,m*x_axis+q)
        plt.setp(ax1.get_xticklabels(),visible=False)
        plt.ylabel('U/V')
        plt.figtext(0.15,0.73,' a = ({:.2e} $\pm$ {:.2e})V/K$^4$ \n b = ({:.3f} $\pm$ {:.3f})V \n $\chi^2 /ndof = {:.2f}$'.format(m,em,q,eq,chiq_ndof))
        
        ax2 = plt.subplot(212,sharex=ax1)
        plt.errorbar(T4, (U-m*T4-q) , yerr = np.sqrt(eU**2+m**2*eT4**2), linestyle='None')
        plt.axhline(0)
        plt.xlabel('$T^4-T_0^4 / K^4$')
        plt.ylabel('Residuen')
        
        plt.show()
        
        print eq/q, chiq_ndof
        
        return m,em,q,eq

w=Auswertung(h.get_werte('weiss'),1)
m=Auswertung(h.get_werte('messing'),2)
s=Auswertung(h.get_werte('schwarz'),3)
sp=Auswertung(h.get_werte('spiegel'),4)
