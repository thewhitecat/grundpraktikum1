# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 14:12:28 2017

@author: Tim
"""

import numpy as np
import Praktikum
import matplotlib.pyplot as plt


data = np.genfromtxt("Kalibration_A.txt",delimiter = ",",skip_header = 1)
m, s = data[:,0], data[:,1]

s_error = np.full(len(s),0.01/np.sqrt(12))

a,ea,b,eb,chiq,cov = Praktikum.lineare_regression(m,s,s_error)
chiq_ndof = chiq/(len(s)-2)
x_axis = np.linspace(0,85,100)


plt.figure()

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


l = 632.8e-9
el = 0.1e-9

a = a*1e-3
ea = ea*1e-3

k = l/(2*a)
ek = k*np.sqrt((el/l)**2+(ea/a)**2)

print k,ek









