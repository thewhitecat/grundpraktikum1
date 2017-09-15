# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:36:42 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

def plot1(yerr,offset):
    plt.errorbar(freq,Utief,marker = '.',yerr=yerr)
    plt.errorbar(freq,Utief-offset,marker = '.',yerr=yerr)
    plt.errorbar(freq,Utief+offset,marker = '.',yerr=yerr)
    plt.errorbar(freq,Uhoch,marker = '.',yerr=yerr)
    plt.errorbar(freq,Uhoch-offset,marker = '.',yerr=yerr)
    plt.errorbar(freq,Uhoch+offset,marker = '.',yerr=yerr)
    plt.plot(freq,np.full(len(freq),Uin_mean/np.sqrt(2)))
    
def plot2():
    plt.plot(freq,Utief)
    x = np.linspace(0,3000,1000)
    plt.plot(x,1./(np.sqrt(1+(x*(2*np.pi)*99.08*4.5974*10**(-6))**2))*Uin_mean)
    plt.plot(freq,np.full(len(freq),1./np.sqrt(2)))

def plot3():
    plt.plot(freq,Uhoch/Uin_mean)
    x = np.linspace(0,3000,1000)
    plt.plot(x,1./(np.sqrt(1+(1./(x*(2*np.pi)*99.08*4.5974*10**(-6)))**2)),linestyle='dashed')
    plt.plot(freq,np.full(len(freq),1./np.sqrt(2)))

messung1=p.lese_lab_datei('pass2.lab')
#Index,zeit,Uin,Iin,phi,UA2,UB2,?,f0,f1,z,hoch,tief
freq = messung1[:,9]
Uin = messung1[:,2]
Uin_mean = np.mean(Uin)
Uhoch = messung1[:,5]
Utief = messung1[:,6]-(messung1[0,6]-Uin_mean)
Uin_mean = np.mean(Uin)
Uin_std = np.std(Uin)
yerr=np.sqrt(Uin_std**2 + (0.0*3)**2)
#freq_hoch = 350
#freq_hoch_max = 349.5
#freq_hoch_min = 350.6
#freq_hoch_err = 0.9
#freq_tief = 351.6
#tieferr = 1.1

#freq_schnitt = 350.8
freq_erwartung = 1./(2*np.pi*99.08*4.5974*10**(-6))
plot1(yerr,-yerr)
stds = (350.-freq_erwartung)/0.9