# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:12:15 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt

messung1=p.lese_lab_datei('Parallell_unendlich2.lab')
#Index,zeit,Uin,Iin,phi,IA2,UB2,?,IA3,f0,f1,z,hoch,tief
freq = messung1[:,10]
Uin = messung1[:,2]
Iin = messung1[:,3]
UR = messung1[:,6]
IC = messung1[:,5]
IL = messung1[:,8]
phi = messung1[:,4]/360*(2*np.pi)
plt.plot(freq,Iin)
plt.plot(freq,phi)
plt.plot(freq,IC)
plt.plot(freq,IL)
err = np.std(Uin)
def func(x,a,b,c,d,e,f):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5

def func2(x,a,b,d):
    return np.arctan((x+d)*a)+b

xwerte = np.linspace(1000,3500,1000)
popt,pcov = opt.curve_fit(func,freq,Iin,sigma=np.full(len(freq),err),absolute_sigma=True,p0=[1,1,1,1,1,1])
popt2 = opt.curve_fit(func,freq,IC,p0=[1,1,1,1,1,1])
perr = np.sqrt(np.diag(pcov))
ywerte = func(xwerte,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
plt.plot(xwerte,ywerte)

popt,pcov = opt.curve_fit(func,freq,IC,p0=[1,1,1,1,1,1])
ywerte2 = func(xwerte,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
plt.plot(xwerte,ywerte2)

popt,pcov = opt.curve_fit(func,freq,IL,p0=[1,1,1,1,1,1])
ywerte3 = func(xwerte,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
plt.plot(xwerte,ywerte3)

popt,pcov = opt.curve_fit(func2,freq,phi,p0=[0,0,-2000])
print popt
ywerte4 = func2(xwerte,*popt)
plt.plot(xwerte,ywerte4)

minimum = xwerte[np.argmin(ywerte)]
L=1.275*10**(-3)
C = 4.5975*10**(-6)
Rl = 0.8
w0 = np.sqrt((1-C/L * Rl**2)/(L*C))/(2*np.pi)
