# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:12:15 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt

messung1=p.lese_lab_datei('lab/Parallel_100Ohm.lab')
#Index,zeit,Uin,Iin,phi,IA2,UB2,?,IA3,f0,f1,z,hoch,tief
freq = messung1[:,-2]
Uin = messung1[:,2]
Iin = messung1[:,3]
UR = messung1[:,6]
IC = messung1[:,-6]
IL = messung1[:,-3]
phi = messung1[:,-7]/360*(2*np.pi)
err = np.std(Uin)
Z = Uin/Iin
def func(x,a,b,c,d,e,f,g):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5+g*x**6

def func3(x,a,b):
    return a+b*x

def func4(x,a,b,c):
    return a/(x+c)+b

def func2(x,a,b,c,d):
    return c*np.arctan((x+d)*a)+b

xwerte = np.linspace(freq[0],3500,1000)
def plot1():
    plt.figure(2)
    plt.plot(freq,Iin)
    plt.plot(freq,IC)
    plt.plot(freq,IL)
    
    popt,pcov = opt.curve_fit(func,freq,Iin)#,sigma=errors(Iin),absolute_sigma=True)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)

    popt,pcov = opt.curve_fit(func,freq,IC)#,p0=[1,1])
    ywerte2 = func(xwerte,*popt)
    plt.plot(xwerte,ywerte2)
    
    popt,pcov = opt.curve_fit(func,freq,IL)#,p0=[100,1,1])
    ywerte3 = func(xwerte,*popt)
    plt.plot(xwerte,ywerte3)
    minimum = xwerte[np.argmin(ywerte)]
    print minimum
    
def plot2():
    plt.plot(freq,phi)
    popt,pcov = opt.curve_fit(func2,freq,phi,p0=[1,1,1,-2200])
    print popt
    ywerte4 = func2(xwerte,*popt)
    plt.plot(xwerte,ywerte4)
    plt.plot(xwerte,np.full(len(xwerte),0),color='red',linestyle='dashed')
    
def plot3():
    plt.plot(freq,Iin)
    
    popt,pcov = opt.curve_fit(func,freq,Iin)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)
    
    minimum = xwerte[np.argmin(ywerte)]
    print minimum
    plt.plot(xwerte,np.full(len(xwerte),np.min(ywerte)*np.sqrt(2)),color='red',linestyle='dashed')
    

def errors(array):
    i=0
    err = np.empty(len(array))
    while(i<len(array)):
        if i<4:
            err[i] = 0.001
        else:
            if i>len(array)-5:
                err[i] = 0.01
            else:
                err[i] = (np.std([array[i-4],array[i-3],array[i-2],array[i-1],array[i],array[i+1],array[i+2],array[i+3],array[i+4]]))
        i+=1
    return err


L=1.275*10**(-3)
C = 4.5975*10**(-6)
Rl = 0.8
w0 = np.sqrt((1-C/L * Rl**2)/(L*C))/(2*np.pi)
print w0
plot2()