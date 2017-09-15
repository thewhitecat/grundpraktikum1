# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:12:15 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt

messung1=p.lese_lab_datei('Messung4.lab')
#Index,zeit,Uin,Iin,phi,IA2,UB2,?,IA3,f0,f1,z,hoch,tief
freq = messung1[:,10]
Uin = messung1[:,2]
Iin = messung1[:,3]
UR = messung1[:,6]
IC = messung1[:,5]
IL = messung1[:,8]
phi = messung1[:,4]/360*(2*np.pi)
Z=Uin/Iin
err = np.std(Uin)
def func(x,a,b,c,d,e,f,g):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5+g*x**6

def func2(x,a,b,c,d):
    return c*np.arctan((x+d)*a)+b

def func3(x,a,b):
    return a+b*x

def func4(x,a,b,c):
    return a/(x+c)+b

def func5(x,a,x0,sigma,b,c):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+b*x+c

xwerte = np.linspace(freq[0],freq[-1],len(freq)*2)
def plot1():#alles
    plt.plot(freq,Iin)
    plt.plot(freq,IC)
    plt.plot(freq,IL)
    
    popt,pcov = opt.curve_fit(func,freq,Iin)#,sigma=errors(Iin),absolute_sigma=True)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)
    
    popt,pcov = opt.curve_fit(func3,freq,IC,p0=[1,1])
    ywerte2 = func3(xwerte,*popt)
    plt.plot(xwerte,ywerte2)
    err = fehler(IC,ywerte2)
    plt.plot(xwerte,ywerte2+err)
    plt.plot(xwerte,ywerte2-err)
    
    popt,pcov = opt.curve_fit(func4,freq,IL,p0=[100,1,1])
    ywerte3 = func4(xwerte,*popt)
    plt.plot(xwerte,ywerte3)
    err = fehler(IL,ywerte3)
    plt.plot(xwerte,ywerte3+err)
    plt.plot(xwerte,ywerte3-err)
    
    argmin = np.argmin(ywerte)
    minimum = xwerte[argmin]
    schnittpunkt = np.argmin(np.abs(ywerte2-ywerte3))
    print minimum
    print xwerte[schnittpunkt],ywerte3[schnittpunkt],err
    print 'Q_L=',ywerte3[schnittpunkt]/ywerte[schnittpunkt]
    print 'Q_C=',ywerte2[schnittpunkt]/ywerte[schnittpunkt]
    
def plot2():#Phase
    plt.plot(freq,phi)
    popt,pcov = opt.curve_fit(func2,freq,phi,p0=[1,1,1,-2200])
    print popt
    ywerte4 = func2(xwerte,*popt)
    plt.plot(xwerte,ywerte4)
    plt.plot(xwerte,np.full(len(xwerte),0),color='red',linestyle='dashed')
    plt.plot(xwerte,np.full(len(xwerte),1./np.sqrt(2)),color='yellow',linestyle='dashed')
    plt.plot(xwerte,np.full(len(xwerte),-1./np.sqrt(2)),color='yellow',linestyle='dashed')
    
def plot3():#Breite Iges
    plt.plot(freq,Iin)
    
    popt,pcov = opt.curve_fit(func,freq,Iin)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)
    err = fehler(Iin,ywerte)
    print (np.sqrt(4*err**2))
    minimum = xwerte[np.argmin(ywerte)]
    print minimum
    plt.plot(xwerte,np.full(len(xwerte),np.min(ywerte)*np.sqrt(2)),color='red',linestyle='dashed')
    plt.plot(xwerte,np.full(len(xwerte),(np.min(ywerte)+err)*np.sqrt(2)),color='green',linestyle='dashed')
    plt.plot(xwerte,np.full(len(xwerte),(np.min(ywerte)-err)*np.sqrt(2)),color='green',linestyle='dashed')

def plot4(plotte):#Gaussfit Z
    popt,pcov = opt.curve_fit(func5,freq,Z,p0=[1,2200,1000,0,1],maxfev = 5000)
    ywerte = func5(xwerte,*popt)
    if plotte == True:
        plt.plot(freq,Z)
        plt.plot(xwerte,ywerte)
    wres = xwerte[np.argmax(ywerte)]
    maxi = np.max(ywerte)
    return wres,maxi

def plot5(plotte):#Polynom Z
    popt,pcov = opt.curve_fit(func,freq,Z)
    ywerte = func(xwerte,*popt)
    if plotte == True:
        plt.plot(freq,Z)
        plt.plot(xwerte,ywerte)
    wres = xwerte[np.argmax(ywerte)]
    maxi = np.max(ywerte)
    return wres,maxi

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

def fehler(array, anpassung):
    i = 0
    err = np.empty(len(array))
    while(i<len(array)):
        err[i] = np.abs(anpassung[2*i]-array[i])
        i+=1
    return np.std(err)



L=1.275*10**(-3)
C = 4.5975*10**(-6)
Rl = 0.8
R = 99.08
w0 = np.sqrt((1-C/L * Rl**2)/(L*C))/(2*np.pi)
print w0
wres,Zmax = plot5(False)
print 'Q=',R*np.sqrt(C/L)/(1+R*Rl*C/L)
print 'Q2=',1./Rl * np.sqrt(L/C)
print 'Q_Z=',wres*2*np.pi*C*Zmax
plot1()