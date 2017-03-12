# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:32:31 2017

@author: Tim
"""

import sys
sys.path.append('C:\Users\Tim\Desktop\Praktikum\Python\Bib')
import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

data1=p.lese_lab_datei('Resonanzen.lab')
data2=p.lese_lab_datei('Resonanzen2.lab')

L=42.8#cm
eL=0.5#cm

vol1=data1[:,2]#V
freq1=data1[:,3]#Hz
vol2=data2[:,2]
freq2=data2[:,3]

#plt.plot(freq1,vol1)


#intervalle
f_1,v_1=p.untermenge_daten(freq1,vol1,400-120,400+120)
f_2,v_2=p.untermenge_daten(freq1,vol1,800-120,800+120)
f_3,v_3=p.untermenge_daten(freq1,vol1,1200-120,1200+120)
f_4,v_4=p.untermenge_daten(freq1,vol1,1600-120,1600+120)
f_5,v_5=p.untermenge_daten(freq1,vol1,2000-120,2000+120)
f_6,v_6=p.untermenge_daten(freq1,vol1,2400-120,2400+120)

def func(x,y,lower,upper):
    liste=[]
    
    for i in range(11):
#       links=p.untermenge_daten(x,y,lower+i*10,upper)
#        rechts=p.untermenge_daten(x,y,lower,upper-i*10)
#        beide=p.untermenge_daten(x,y,lower+i*10,upper-i*10)
        
        b1=p.peak(x,y,lower+i*10,upper)
        b2=p.peak(x,y,lower,upper-i*10)
        b3=p.peak(x,y,lower+i*10,upper-i*10)
        
        liste.append(b1)
        liste.append(b2)
        liste.append(b3)
         
    return np.mean(liste),np.std(liste,ddof=1)
      
f1,sf1=func(f_1,v_1,400-120,400+120)
f2,sf2=func(f_2,v_2,800-120,800+120)
f3,sf3=func(f_3,v_3,1200-120,1200+120)
f4,sf4=func(f_4,v_4,1600-120,1600+120)
f5,sf5=func(f_5,v_5,2000-120,2000+120)
f6,sf6=func(f_6,v_6,2400-120,2400+120) 

f=np.array([f1,f2,f3,f4,f5,f6])
sf=np.array([sf1,sf2,sf3,sf4,sf5,sf6])
n=np.arange(1,7,1)

a,ea,b,eb,chiq,cov=p.lineare_regression(n,f,sf)       

#print(chiq/4)      
   
fig1, ax1=plt.subplots(2,1,sharex=True)
ax1[0].set_title('Geradenanpassung und Residuen')
ax1[0].set_ylabel('f/Hz')
ax1[1].set_ylabel('f/Hz')
ax1[0].errorbar(n,f,sf,fmt='.',linestyle='None',label='Messpunkte')
ax1[0].plot(n,a*n+b,label='Anpassungsgerade')
ax1[0].legend()
ax1[1].set_xlabel('n')
ax1[1].errorbar(n,f-a*n-b,sf,linestyle='None',fmt='o')
ax1[1].axhline(0,color='black',linestyle='dashed')



