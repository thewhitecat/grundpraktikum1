# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:39:49 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt

def einlesen(string):
    Messing1=p.lese_lab_datei(string + '/mes50.lab')
    Messing2=p.lese_lab_datei(string + '/mes55.lab')
    Messing3=p.lese_lab_datei(string + '/mes60.lab')
    Messing4=p.lese_lab_datei(string + '/mes65.lab')
    Messing5=p.lese_lab_datei(string + '/mes70.lab')
    Messing6=p.lese_lab_datei(string + '/mes75.lab')
    Messing7=p.lese_lab_datei(string + '/mes80.lab')
    Messing8=p.lese_lab_datei(string + '/mes85.lab')
    Messing9=p.lese_lab_datei(string +'/mes90.lab')
    Messing10=p.lese_lab_datei(string + '/mes95.lab')
    temp = [Messing1[:,3],Messing2[:,3],Messing3[:,3],Messing4[:,3],Messing5[:,3],Messing6[:,3],Messing7[:,3],Messing8[:,3],Messing9[:,3],Messing10[:,3]]
    U = [Messing1[:,2],Messing2[:,2],Messing3[:,2],Messing4[:,2],Messing5[:,2],Messing6[:,2],Messing7[:,2],Messing8[:,2],Messing9[:,2],Messing10[:,2]]
    return temp, U
temp_mean = np.zeros(10)
temp_std = np.zeros(10)
U_mean = np.zeros(10)
U_std = np.zeros(10)
def histogramm(temp, U,bilder):
    if bilder == 1:
        f,ax = plt.subplots(len(temp)-5,2)
    for i in range(len(temp)-5):
        temp_mean[i] = np.mean(temp[i])
        temp_std[i] = np.std(temp[i],ddof=1)/np.sqrt(len(temp[i]))
        U_mean[i] = np.mean(U[i])
        U_std[i] = np.std(U[i],ddof=1)/np.sqrt(len(U[i]))
        if bilder == 1:
            ax[i,0].hist(temp[i])
            ax[i,0].set_title('Temperatur {}C'.format(i*5+50))
            ax[i,0].set_xlabel('T in C')
            ax[i,0].set_ylabel('#')
            ax[i,0].legend
            ax[i,0].text(0.95, 0.95, ' mean={}C \n err={}C'.format(round(temp_mean[i],2),round(temp_std[i],2)),verticalalignment='top', horizontalalignment='right',transform=ax[i,0].transAxes,color='red', fontsize=10)
            ax[i,1].hist(U[i])
            ax[i,1].set_title('Spannung {}C'.format(i*5+50))
            ax[i,1].set_xlabel('U in V')
            ax[i,1].set_ylabel('#')
            ax[i,1].text(0.95, 0.95, ' mean={}V \n err={}V'.format(round(U_mean[i],4),round(U_std[i],4)),verticalalignment='top', horizontalalignment='right',transform=ax[i,1].transAxes,color='red', fontsize=10)
    if bilder == 1:
        #f.tight_layout()
        f,ax = plt.subplots(len(temp)-5,2)
    for i in range(len(temp)-5):
        if bilder == 1:
            ax[i,0].hist(temp[i+5])
            ax[i,0].set_title('Temperatur {}C'.format(i*5+50))
            ax[i,0].set_xlabel('T in C')
            ax[i,0].set_ylabel('#')
            ax[i,1].hist(U[i+5])
            ax[i,1].set_title('Spannung {}C'.format((i+5)*5+50))
            ax[i,1].set_xlabel('U in V')
            ax[i,1].set_ylabel('#')
        temp_mean[i+5] = np.mean(temp[i+5])
        temp_std[i+5] = np.std(temp[i+5],ddof=1)/np.sqrt(len(temp[i+5]))
        U_mean[i+5] = np.mean(U[i+5])
        U_std[i+5] = np.std(U[i+5],ddof=1)/np.sqrt(len(U[i+5]))
    #if bilder == 1:
        #f.tight_layout()

def get_werte(string):
    temp, U = einlesen(string)
    histogramm(temp,U,0)
    return temp_mean,temp_std,U_mean,U_std

if __name__ == "__main__":
    temp, U = einlesen('schwarz')
    histogramm(temp,U,1)