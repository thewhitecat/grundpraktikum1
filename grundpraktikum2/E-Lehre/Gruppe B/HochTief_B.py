# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:36:45 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum
import scipy.optimize as opt

R = 9.988
C = 4.475e-6

data = Praktikum.lese_lab_datei('lab/Hoch-Tief.lab')

U_1 = data[:,2]
U_0,rauschen = np.mean(U_1), np.std(U_1,ddof = 1)


f = data[:,-2]

#offset von vormessen
U_tief = data[:,-3]+0.00492
U_hoch = data[:,-6]-0.0152371
phase = data[:,4]
#U_tief = data[:,-3]
#U_hoch = data[:,-6]


#tief,hoch = U_tief/U_0,U_hoch/U_0
errs = np.full(len(U_tief),rauschen)

plt.figure(4)
plt.plot(f[1:-1],phase[1:-1])
plt.xlabel('$f$/Hz')
plt.ylabel('$\phi$/deg')
plt.axhline(45,linestyle='dashed')
plt.show()


plt.figure(0)
plt.errorbar(f,U_tief,yerr=errs)
plt.errorbar(f,U_hoch,yerr=errs)
plt.axhline(U_0/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.ylabel('$U_a$/V')
plt.xlabel('$f$/Hz')

x=np.linspace(0.00001,8000,10000)
#plt.plot(x,U_0/np.sqrt((1/(x*2*np.pi*R*C))**2+1))
#plt.plot(x,U_0/np.sqrt(1+(x*2*np.pi*C*R)**2))
plt.show()


plt.figure(1)
plt.title('Systematischer Fehler subtrahiert')
U_tief = data[:,-3]*0.99
U_hoch = data[:,-6]*0.99
errs = np.full(len(U_tief),rauschen)
plt.errorbar(f,U_tief,yerr=errs)
plt.errorbar(f,U_hoch,yerr=errs)
plt.axhline((U_0)/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.show()

plt.figure(2)
plt.title('Systematischer Fehler addiert')
U_tief = data[:,-3]*1.01
U_hoch = data[:,-6]*1.01
errs = np.full(len(U_tief),rauschen)
plt.errorbar(f,U_tief,yerr=errs)
plt.errorbar(f,U_hoch,yerr=errs)
plt.axhline(U_0/np.sqrt(2), linestyle = 'dashed',color = 'red')
plt.show()










#anoassung probiert, totaler mist...
'''
def f1(x,w0):
    return 1/np.sqrt(w0**2/(2*np.pi*x)**2+1)

def f2(x,w0):
    return 1/np.sqrt(1+((x*2*np.pi)**2/w0**2))

popt1,pcov1 = opt.curve_fit(f1,f,hoch,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)
popt2,pcov2 = opt.curve_fit(f2,f,tief,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)

plt.plot(x,f1(x,*popt1))
plt.plot(x,f2(x,*popt2))

print popt1/(2*np.pi),popt2/(2*np.pi)


def func_oben(popt1=popt1,popt2=popt2):
    U_tief = data[:,-3]*(1+0.001)+0.0005*7
    U_hoch = data[:,-6]*(1+0.001)+0.0005*7
    tief,hoch = U_tief/U_0,U_hoch/U_0
    errs = np.full(len(tief),rauschen/U_0)
    p1,cov1 = opt.curve_fit(f1,f,hoch,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)
    p2,cov2 = opt.curve_fit(f2,f,tief,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)
    
    return (p1-popt1)/(2*np.pi),(p2-popt2)/(2*np.pi)
    

def func_unten(popt1=popt1,popt2=popt2):
    U_tief = data[:,-3]*(1-0.001)-0.0005*7
    U_hoch = data[:,-6]*(1-0.001)-0.0005*7
    tief,hoch = U_tief/U_0,U_hoch/U_0
    errs = np.full(len(tief),rauschen/U_0)
    p1,cov1 = opt.curve_fit(f1,f,hoch,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)
    p2,cov2 = opt.curve_fit(f2,f,tief,p0=[np.pi*3500],absolute_sigma = True, sigma = errs)

    return (p1-popt1)/(2*np.pi),(p2-popt2)/(2*np.pi)

fehler_oben = func_oben()
fehler_unten = func_unten()

print fehler_oben
print fehler_unten


chiq=0
for i in range(len(tief)):
    chiq = chiq + (tief[i]-f2(f[i],*popt1))**2/errs[i]**2
    
chiq_ndof = chiq/(len(tief)-1)
'''














