# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 14:14:03 2017

@author: morit
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

def linreg(data, xerr, yerr):
    a,ea,b,eb,chiq,cov = p.lineare_regression(m,data,xerr,yerr)
    chiq_ndof = chiq/(len(m)-2)
    x_axis = np.linspace(0,85,100)
    
    ax1 = plt.subplot(211)
    plt.errorbar(m,s,s_error,linestyle = 'None',marker = '.')
    plt.plot(x_axis,a*x_axis+b)
    plt.ylabel('s/mm')
    plt.figtext(0.15,0.70,' a = {}$\pm${} \n b = {}$\pm${} \n $\chi^2/ndof$ = {}'.format(round(a,5),round(ea,5),round(b,5),round(eb,5),round(chiq_ndof,3)))
    plt.setp(ax1.get_xticklabels(),visible=False)
    
    ax2 = plt.subplot(212,sharex=ax1)
    plt.errorbar(m,s-(m*a+b),s_error,linestyle = 'None')
    plt.axhline(0)
    plt.xlabel('m')
    plt.ylabel('Residuen')
    plt.show()

data_raw = np.genfromtxt('Druck_A.txt', delimiter = ',', skip_header = 2);
m = np.array(data_raw[:,0])
data1 = np.array(data_raw[:,1])
data2 = np.array(data_raw[:,2])
data3 = np.array(data_raw[:,3])
data4 = np.array(data_raw[:,4])
data5 = np.array(data_raw[:,5])
data6 = np.array(data_raw[:,6])

