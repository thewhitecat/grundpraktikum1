# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:39:49 2017

@author: morit
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt
import untitled0 as seb

def einlesen(string):
    Messing1=p.lese_lab_datei(string + '/50.lab')
    Messing2=p.lese_lab_datei(string + '/55.lab')
    Messing3=p.lese_lab_datei(string + '/60.lab')
    Messing4=p.lese_lab_datei(string + '/65.lab')
    Messing5=p.lese_lab_datei(string + '/70.lab')
    Messing6=p.lese_lab_datei(string + '/75.lab')
    Messing7=p.lese_lab_datei(string + '/80.lab')
    Messing8=p.lese_lab_datei(string + '/85.lab')
    Messing9=p.lese_lab_datei(string +'/90.lab')
    Messing10=p.lese_lab_datei(string + '/95.lab')
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
            ax[i,0].text(0.95, 0.95, ' mean={}C \n err={}C'.format(round(temp_mean[i],2),round(temp_std[i],2)),verticalalignment='top', horizontalalignment='right',transform=ax[i,0].transAxes,color='red', fontsize=10)
            test = sorted(U[i])
            binwidth = 100.
            for x in range(len(U[i])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,1].hist(U[i],bins=np.arange(min(U[i]), max(U[i]) + 2* binwidth, binwidth))
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
            test = sorted(U[i+5])
            binwidth = 100.
            for x in range(len(U[i+5])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,1].hist(U[i+5],bins=np.arange(min(U[i+5]), max(U[i+5]) + 2*binwidth, binwidth))
            ax[i,1].set_title('Spannung {}C'.format((i+5)*5+50))
            ax[i,1].set_xlabel('U in V')
            ax[i,1].set_ylabel('#')
        temp_mean[i+5] = np.mean(temp[i+5])
        temp_std[i+5] = np.std(temp[i+5],ddof=1)/np.sqrt(len(temp[i+5]))
        U_mean[i+5] = np.mean(U[i+5])
        U_std[i+5] = np.std(U[i+5],ddof=1)/np.sqrt(len(U[i+5]))
    #if bilder == 1:
        #f.tight_layout()
        
def histogramm2(temp, U,bilder):
    if bilder == 1:
        f,ax = plt.subplots(len(temp)-5,4)
    for i in range(len(temp)-5):
        temp_mean[i] = np.mean(temp[i])
        temp_std[i] = np.std(temp[i],ddof=1)/np.sqrt(len(temp[i]))
        U_mean[i] = np.mean(U[i])
        U_std[i] = np.std(U[i],ddof=1)/np.sqrt(len(U[i]))
        if bilder == 1:
            test = sorted(temp[i])
            binwidth = 100.
            for x in range(len(temp[i])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,0].hist(temp[i],color = '#66ccff',bins=np.arange(min(temp[i]), max(temp[i]) + 2* binwidth, binwidth),)
            ax[i,0].set_title('Temperatur {}C'.format(i*5+50))
            ax[i,0].set_xlabel('T in C')
            ax[i,0].text(0.95, 0.95, ' mean={}C \n err={}C'.format(round(temp_mean[i],3),round(temp_std[i],3)),verticalalignment='top', horizontalalignment='right',transform=ax[i,0].transAxes,color='black', fontsize=10)
            test = sorted(U[i])
            binwidth = 100.
            for x in range(len(U[i])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,1].hist(U[i],bins=np.arange(min(U[i]), max(U[i]) + 2* binwidth, binwidth),color = '#66ccff')
            ax[i,1].set_title('Spannung {}C'.format(i*5+50))
            ax[i,1].set_xlabel('U in V')
            ax[i,1].text(0.95, 0.95, ' mean={}V \n err={}V'.format(round(U_mean[i],4),round(U_std[i],4))
            ,verticalalignment='top', horizontalalignment='right',transform=ax[i,1].transAxes,color='black', fontsize=10)
    #if bilder == 1:
        #f.tight_layout()
    #    f,ax = plt.subplots(len(temp)-5,2)
    for i in range(len(temp)-5):
        temp_mean[i+5] = np.mean(temp[i+5])
        temp_std[i+5] = np.std(temp[i+5],ddof=1)/np.sqrt(len(temp[i+5]))
        U_mean[i+5] = np.mean(U[i+5])
        U_std[i+5] = np.std(U[i+5],ddof=1)/np.sqrt(len(U[i+5]))
        if bilder == 1:
            binwidth = 100.
            test = sorted(temp[i+5])
            for x in range(len(temp[i+5])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,2].hist(temp[i+5],color = '#66ccff',bins=np.arange(min(temp[i+5]), max(temp[i+5]) + 2*binwidth, binwidth))
            ax[i,2].set_title('Temperatur {}C'.format((i+5)*5+50))
            ax[i,2].set_xlabel('T in C')
            ax[i,2].text(0.95, 0.95, ' mean={}V \n err={}V'.format(round(temp_mean[i+5],3),round(temp_std[i+5],3))
            ,verticalalignment='top', horizontalalignment='right',transform=ax[i,2].transAxes,color='black', fontsize=10)
            test = sorted(U[i+5])
            binwidth = 100.
            for x in range(len(U[i+5])-1):
                if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
                    binwidth = np.abs(test[x]-test[x+1])
            ax[i,3].hist(U[i+5],bins=np.arange(min(U[i+5]), max(U[i+5]) + 2*binwidth, binwidth),color = '#66ccff')
            ax[i,3].set_title('Spannung {}C'.format((i+5)*5+50))
            ax[i,3].set_xlabel('U in V')
            ax[i,3].text(0.95, 0.95, ' mean={}V \n err={}V'.format(round(U_mean[i+5],4),round(U_std[i+5],4))
            ,verticalalignment='top', horizontalalignment='right',transform=ax[i,3].transAxes,color='black', fontsize=10)
    #if bilder == 1:
        #f.tight_layout()
def beispiel(temp, U):
    test = sorted(temp[4])
    binwidth = 100.
    for x in range(len(temp[4])-1):
        if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
            binwidth = np.abs(test[x]-test[x+1])
    plt.figure(4)
    plt.hist(temp[4],bins=np.arange(min(temp[4]), max(temp[4]) + 2*binwidth, binwidth))
    plt.title('Temperatur {}C'.format(4*5+50))
    plt.xlabel('T in C')
    plt.ylabel('#')
    #plt.figtext(0.2,0.7,' mean={}C \n err={}C'.format(round(temp_mean[4],2),round(temp_std[4],2)))
    plt.figure(5)
    test = sorted(U[4])
    binwidth = 100.
    for x in range(len(U[4])-1):
        if binwidth > np.abs(test[x]-test[x+1]) and np.abs(test[x]-test[x+1]) != 0.0:
            binwidth = np.abs(test[x]-test[x+1])
    plt.hist(U[4],bins=np.arange(min(U[4]), max(U[4]) + 2*binwidth, binwidth))
    plt.title('Spannung {}C'.format(4*5+50))
    plt.xlabel('U in V')
    plt.ylabel('#')

def get_werte(string):
    temp, U = einlesen(string)
    histogramm(temp,U,0)
    return temp_mean,temp_std,U_mean,U_std

if __name__ == "__main__":
    temp, U = einlesen('C/messing')
    #histogramm2(temp,U,1)
    beispiel(temp,U)