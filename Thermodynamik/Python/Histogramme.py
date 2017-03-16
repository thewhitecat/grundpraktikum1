# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:36:18 2017

@author: Tim
"""

import Praktikum as p
import matplotlib.pyplot as plt
import numpy as np


data_a=p.lese_lab_datei('CASSY/Rauschmessungen.lab')
druck_a=data_a[:,2]
temp_a=data_a[:,3]

data_b=p.lese_lab_datei('Lab/Rauschmessungen.lab')
druck_b=data_b[:,4]
temp_b=data_b[:,2]

def stat(x):
    return np.mean(x),np.std(x,ddof=1)

def gauss(x,m,s):
    return 1/(np.sqrt(2*np.pi*s**2))*np.exp(-(x-m)**2/s**2)


#druck a
m_a_druck,s_a_druck=stat(druck_a)
x=np.linspace(993,994.5,1000)
bins_a_druck=np.arange(993-0.375,995.25-0.375,0.75)
plt.figure(1)
plt.hist(druck_a,bins=bins_a_druck,normed=True)
#plt.xticks()
plt.plot(x,gauss(x,m_a_druck,s_a_druck),color='red')
plt.xlabel('Druck [hPa]')
plt.ylabel('#')
plt.title('Druckrauschen Versuch A')
plt.figtext(0.2,0.7,
            '\n$\mu=$'+str(np.round(m_a_druck,2))+'hPa\n'
            +'$\sigma=$'+str(np.round(s_a_druck,2))+'hPa')

#temp a
m_a_temp,s_a_temp=stat(temp_a)
x=np.linspace(1.5,3,1000)
bins_a_temp=np.arange(1.5,2.75,0.1)
plt.figure(2)
plt.hist(temp_a,bins=bins_a_temp,normed=True)
plt.plot(x,gauss(x,m_a_temp,s_a_temp),color='red')
plt.xlabel('Temperatur [C]')
plt.ylabel('#')
plt.title('Temperaturrauschen Versuch A')
plt.figtext(0.2,0.7,
            '\n$\mu=$'+str(np.round(m_a_temp,2))+'C\n'
            +'$\sigma=$'+str(np.round(s_a_temp,2))+'C')


#druck b
m_b_druck,s_b_druck=stat(druck_b)
x=np.linspace(1020,1022.5,1000)
bins_b_druck=np.arange(1020-0.375,1023.75-0.375,0.75)
plt.figure(3)
plt.hist(druck_b,bins=bins_b_druck,normed=True)
plt.plot(x,gauss(x,m_b_druck,s_b_druck),color='red')
plt.xlabel('Druck [hPa]')
plt.ylabel('#')
plt.title('Druckrauschen Versuch B')
plt.figtext(0.2,0.7,
            '\n$\mu=$'+str(np.round(m_b_druck,2))+'hPa\n'
            +'$\sigma=$'+str(np.round(s_b_druck,2))+'hPa')


#temp b
m_b_temp,s_b_temp=stat(temp_b)
x=np.linspace(22.5,23.3,1000)
bins_b_temp=np.arange(22.7,23.3,0.1)
plt.figure(4)
plt.hist(temp_b,bins=bins_b_temp,normed=True)
plt.plot(x,gauss(x,m_b_temp,s_b_temp),color='red')
plt.xlabel('Temperatur [C]')
plt.ylabel('#')
plt.title('Temperaturrauschen Versuch B')
plt.figtext(0.2,0.7,
            '\n$\mu=$'+str(np.round(m_b_temp,2))+'C\n'
            +'$\sigma=$'+str(np.round(s_b_temp,2))+'C')


















