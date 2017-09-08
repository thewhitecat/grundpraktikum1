# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 14:14:03 2017

@author: morit
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

def linreg(m,data1,xerr, yerr):
    a,ea,b,eb,chiq,cov = p.lineare_regression_xy(m,data1,xerr, yerr)
    chiq_ndof = chiq/(len(m)-2)
    x_axis = np.linspace(0,10,100)
    plt.figure()
    ax1 = plt.subplot(211)
    plt.errorbar(m,data1,xerr = xerr,yerr = yerr,linestyle = 'None',marker = '.')
    plt.plot(x_axis,a*x_axis+b)
    plt.ylabel('s/mm')
    plt.figtext(0.15,0.70,' a = {}$\pm${} \n b = {}$\pm${} \n $\chi^2/ndof$ = {}'.format(round(a,5),round(ea,5),round(b,5),round(eb,5),round(chiq_ndof,3)))
    plt.setp(ax1.get_xticklabels(),visible=False)
    
    ax2 = plt.subplot(212,sharex=ax1)
    plt.errorbar(m,data1-(m*a+b),np.sqrt(yerr**2+(a*xerr)**2),linestyle = 'None')
    plt.axhline(0)
    plt.xlabel('m')
    plt.ylabel('Residuen')
    plt.show()
    return a,ea,chiq_ndof

data_raw = np.genfromtxt('Druck_A.txt', delimiter = ',', skip_header = 1);
m = np.array(data_raw[:,0])
data1 = np.array(data_raw[:,1])
data2 = np.array(data_raw[:,2])
data3 = np.array(data_raw[:,3])
data4 = np.array(data_raw[:,4])
data5 = np.array(data_raw[:,5])
data6 = np.array(data_raw[:,6])

xerr = np.full(len(m),0.2/np.sqrt(12))
yerr = np.full(len(data1),1./np.sqrt(12))

a1,ea1,chi1= linreg(m,data1,xerr,yerr)
a2,ea2,chi2= linreg(m,data2,xerr,yerr)
a3,ea3,chi3= linreg(m,data3,xerr,yerr)
a4,ea4,chi4= linreg(m,data4,xerr,yerr)
a5,ea5,chi5= linreg(m,data5,xerr,yerr)
a6,ea6,chi6= linreg(m,data6,xerr,yerr)

a = np.array([a1,a2,a3,a4,a5,a6])
ea = np.array([ea1,ea2,ea3,ea4,ea5,ea6])
chi = np.array([chi1,chi2,chi3,chi4,chi5,chi6])
gmean,gstd = p.gewichtetes_mittel(a,abs(chi-1))
a_mean = np.mean(a)
a_std = np.std(a)
#a_mean = gmean
#a_std = gstd
print a_mean, a_std
lam = 522.66e-9
lamstat = 0
#lamstat = 2.03e-9
lamsys = np.sqrt(1.92e-9**2+ 2.03e-9**2)
L = 0.01
Lerr = 0
dn = lam/(2.*L*a_mean)
dnerr = dn * np.sqrt((a_std / a_mean)**2 + (lamstat/lam)**2)
dnsys = np.sqrt((dn/L*Lerr)**2 + (dn/lam*lamsys)**2)
print dn,dnerr,dnsys



