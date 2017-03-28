# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:16:57 2017

@author: grldm
"""

import Praktikum as p
import numpy as np
import timeit
from pylab import *
import matplotlib.pyplot as plt
import auswertung_01 as aus

start_time=timeit.default_timer()

#plotte rohdaten und fft
def plots(t=None,U=None,fft=0):
    if t!=None and U!=None:
        plt.subplots()
        plt.plot(t,U)
        plt.ylabel("Spannung[V]")
        plt.xlabel("Zeit[s]")
        plt.title("Rohdaten Kugel")
    if fft==1:
        freq,amp=p.fourier_fft(t,U)
        freq,amp=p.untermenge_daten(freq,amp,0,3)
        plt.subplots()
        plt.plot(freq,amp)
        peak = p.peakfinder_schwerpunkt(freq,amp)
        x=plt.axvline(peak,color='r',label="{}Hz".format(np.round(peak,3)))
        plt.legend(handles=[x],bbox_to_anchor=(1, 1))
        plt.ylabel("#")
        plt.xlabel("Frequenz[Hz]")
        plt.title("FFT der Rohdaten")

def Kugel(feder=2):
    t0 = []
    t1 = []
    for i in range(10):
        data = p.lese_lab_datei("lab/Feder{:1d}/Kugel/messung{:1d}.lab".format(feder, i+1))
        t = data[:,1]
        U = data[:,2]
        if 2 == 1:
            plots(t[:7400], U[:7400], 1)
        
        indizes = aus.get_peaks(t[:t.size*3/4], U[:U.size*3/4])
        indizes = indizes[:13]
        
        t0.append(t[indizes[0]])
        t1.append(t[indizes[-1]])
        
    t0 = np.array(t0)
    t1 = np.array(t1)
    #zwischenergebnis = t1 - t0
    #print zwischenergebnis
    #periodendauer = 2 * zwischenergebnis/12
    #print periodendauer
    
    sig_t0 = np.std(t0, ddof=1)/np.sqrt(t0.size) 
    sig_t1 = np.std(t1, ddof=1)/np.sqrt(t1.size)
    
    t0 = np.mean(t0)
    t1 = np.mean(t1)
    
    T = 2*(t1-t0)/(indizes.size-1)
    sig_T = 2*(sig_t0+sig_t1)/(indizes.size-1)
    
    return T, sig_T

def Scheibe(feder=2):
    t0 = []
    t1 = []
    for i in range(10):
        data = p.lese_lab_datei("lab/Feder{:1d}/Scheibe/messung{:1d}.lab".format(feder, i+1))
        t = data[:,1]
        U = data[:,2]
        
        indizes = aus.get_peaks(t[:t.size*3/4], U[:U.size*3/4])
        indizes = indizes[:14]
        
        t0.append(t[indizes[0]])
        t1.append(t[indizes[-1]])
        
    t0 = np.array(t0)
    t1 = np.array(t1)
    #zwischenergebnis = t1 - t0
    #print zwischenergebnis
    #periodendauer = zwischenergebnis/13
    #print periodendauer
    
    sig_t0 = np.std(t0, ddof=1)/np.sqrt(t0.size) 
    sig_t1 = np.std(t1, ddof=1)/np.sqrt(t1.size)
    
    t0 = np.mean(t0)
    t1 = np.mean(t1)
    
    T = 2*(t1-t0)/(indizes.size-1)
    sig_T = 2*(sig_t0+sig_t1)/(indizes.size-1)
    
    return T, sig_T

#setze Parameter
D = 0.029713
sig_D = np.sqrt((6.8e-5)**2 + 0.0002017**2)
m_scheibe = 0.3352
sig_m_scheibe = 0.0001/np.sqrt(12)
d_scheibe = np.mean([0.224, 0.2249, 0.2235])
sig_d_scheibe = np.std([0.224, 0.2249, 0.2235])
m_kugel = 0.9212
sig_m_kugel = 0.0001/np.sqrt(12)
d_kugel = np.mean([0.1435, 0.144, 0.143, 0.141, 0.1439])
sig_d_kugel = np.std([0.1435, 0.144, 0.143, 0.141, 0.1439])
sys_d_kugel = 0.001 * d_kugel
sys_m_kugel = 0.0001
sys_d_scheibe = 0.001 * d_scheibe
sys_m_scheibe = 0.0001

#berechne exp und theo für scheibe
T_scheibe, sig_T_scheibe = Scheibe()
J_scheibe = 1/(4 * np.pi**2) * D * T_scheibe**2
sig_J_scheibe = 1/(4 * np.pi**2) * np.sqrt((2 * T_scheibe * D * sig_T_scheibe)**2)
J_scheibe_theo = 1./2 * m_scheibe * (d_scheibe/2)**2
sig_J_scheibe_theo = 1./2 * np.sqrt(((d_scheibe/2)**2 * sig_m_scheibe)**2 + (1./2 * m_scheibe * d_scheibe * sig_d_scheibe/2)**2)
sys_J_scheibe = 1/(4 * np.pi**2) * np.sqrt((T_scheibe**2 * sig_D)**2)
sys_J_scheibe_theo = 1./2 * np.sqrt((sys_m_scheibe * (d_scheibe/2)**2)**2 + (sys_d_scheibe * m_scheibe * d_scheibe/2)**2)
           
print("Scheibe: ")
print("experimentell: ", np.round(J_scheibe, 8), " +/- ", np.round(sig_J_scheibe, 8), " +/- ", np.round(sys_J_scheibe, 8))
print ("theoretisch: ", np.round(J_scheibe_theo, 8), " +/- ", np.round(sig_J_scheibe_theo, 8), " +/- ", np.round(sys_J_scheibe_theo, 8))
print("Abweichung: [sigma]: ", np.round(((J_scheibe - J_scheibe_theo - np.sqrt(sig_J_scheibe_theo**2 + sys_J_scheibe_theo**2))/sys_J_scheibe), 3))

#berechne exp und theo für kugel
T_kugel, sig_T_kugel = Kugel()
#print T_kugel, sig_T_kugel
J_kugel = 1/(4 * np.pi**2) * D * T_kugel**2
sig_J_kugel = 1/(4 * np.pi**2) * np.sqrt((2 * T_kugel * D * sig_T_kugel)**2)
sys_J_kugel = 1/(4 * np.pi**2) * np.sqrt((T_kugel**2 * sig_D)**2)
J_kugel_theo = 2./5 * m_kugel * (d_kugel/2)**2
sys_J_kugel_theo = 2./5 * np.sqrt((sys_d_kugel * m_kugel * d_kugel/2)**2 + (sys_m_kugel * (d_kugel/2)**2)**2)
sig_J_kugel_theo = 2./5 * np.sqrt(((d_kugel/2)**2 * sig_m_kugel)**2 + (2 * m_kugel * d_kugel/2 * sig_d_kugel/2)**2)

print("Kugel: ")
print("experimentell: ", np.round(J_kugel, 8), " +/- ", np.round(sig_J_kugel, 8), " +/- ", np.round(sys_J_kugel, 8))
print ("theoretisch: ", np.round(J_kugel_theo, 8), " +/- ", np.round(sig_J_kugel_theo, 8), " +/- ", np.round(sys_J_kugel_theo, 8))
print("Abweichung: [sigma]: ", np.round(((J_kugel - J_kugel_theo - np.sqrt(sig_J_kugel_theo**2 + sys_J_kugel_theo**2))/sys_J_kugel), 3))
            
print("Laufzeit: {0:9.2f} Sekunden".format(timeit.default_timer()-start_time))