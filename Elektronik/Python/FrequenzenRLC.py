# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:44:48 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p


#messung einlesen
messung2=p.lese_lab_datei('lab/19,6Ohm/messung2.lab')
messung3=p.lese_lab_datei('lab/19,6Ohm/messung3.lab')
messung4=p.lese_lab_datei('lab/19,6Ohm/messung4.lab')
messung5=p.lese_lab_datei('lab/19,6Ohm/messung5.lab')
messung1=p.lese_lab_datei('lab/19,6Ohm/messung1.lab')

messungen=[messung1,messung2,messung3,messung4,messung5]
#messung 1 für testzwecke

t1=messung1[:,1]
U1=messung1[:,3]
t4,U4=messung4[:,1],messung4[:,3]
t5,U5=messung5[:,1],messung5[:,3]


def get_offset(U,start=1800):
    werte=U[start:]
    return np.mean(werte)
    




#methode zur bestimmung der frequenzen
def get_freq(messung):
    t=messung[:,1]
    U=messung[:,3]
    U=U-get_offset(U)
    freq,amp=p.fourier_fft(t,U)
    max_index=np.argmax(amp)
    sec=np.argmax([amp[max_index-1],amp[max_index+1]])
    
    if sec==0:
        sec_index=max_index-1
    else:
        sec_index=max_index+1
    
    peak=0.5*(freq[max_index]+freq[sec_index])
    peakerror=(freq[max_index]-freq[sec_index])/np.sqrt(12)
    
    return peak,peakerror

#veraltet
def get_freqa(messung):
    t=messung[:,1]
    U=messung[:,3]
    freq,amp=p.fourier_fft(t,U)
    peak=p.peak(freq,amp,300,400)
    return peak


#peak mittelwerte und fehler und fehler auf mittelwert.
def f_fourier(messungen):
    peaks=[]
    peakerror=[]
    for x in messungen:
        peaks.append(get_freq(x)[0])
        peakerror.append(get_freq(x)[1])
    
#    mean,std=np.mean(peaks),np.std(peaks,ddof=1)
#    mean_error=std/np.sqrt(len(peaks))
    mean,error=p.gewichtetes_mittel(np.array(peaks),np.array(peakerror))
    
#    return mean,std,mean_error
    return mean,None,error

#ab hier versuch durch abzählen...
#erste nullstelle suchen -> dann n nullstellen abzählen -> dann zeit nehmen
def get_zeros(t,U,index_output=True):
    '''
    gibt liste mit Tupeln der Form (t,U,index) zurück,
    dieser index und nächster sind die "nullstellen"
    '''
    U=U-get_offset(U)
    zeros=[]
    for i in range(len(U)-1):
        if U[i]>0 and U[i+1]<0:
            zeros.append((t[i],U[i],i))
        elif U[i]<0 and U[i+1]>0:
            zeros.append((t[i],U[i],i))
        elif U[i]==0 and U[i-1]>0 and i>0:
            zeros.append((t[i],U[i],i))
        elif U[i]==0 and U[i-1]<0 and i>0:
            zeros.append((t[i],U[i],i))
    #don't bother with this stuff   
    
    if index_output==False:
        return zeros
    else:
        index=[]
        for x in zeros:
            index.append((x[2],x[2]+1))
        return index

#wrapper abzähler
#annahme: gleichverteilungsfehler beim abzählen
def f_count(t,U):
    index=get_zeros(t,U)
    times=[]
    error_times=[]
    periods=[]
    error_periods=[]
    
    for x in index:
        times.append((t[x[1]]+t[x[0]])/2)
        error_times.append((t[x[1]]-t[x[0]])/np.sqrt(12))
# hier kommt das 'fitlern' der daten
#werte hangen aufs massivste vom filtern ab...   
    for i in range(len(times)-1):
        if 2*(times[i+1]-times[i])>0.0024 and 2*(times[i+1]-times[i])<0.0030:
            periods.append(2*(times[i+1]-times[i]))
            error_periods.append(2*np.sqrt(error_times[i+1]**2+error_times[i]**2))

    output=p.gewichtetes_mittel(np.array(periods),np.array(error_periods))
    
#    plt.figure()
#    plt.plot(t,U)
#    for x in times:
#        plt.axvline(x)
#    plt.show()

    return(1/output[0],output[1]/output[0]**2)
#    return periods


def wrapper_f_count(messungen):
    f,sigma_f=[],[]
    for x in messungen:
        f.append(f_count(x[:,1],x[:,3])[0])
        sigma_f.append(f_count(x[:,1],x[:,3])[1])
    
    output=p.gewichtetes_mittel(np.array(f),np.array(sigma_f))
    return output


#

def auswertung(messungen):
    fourier=f_fourier(messungen)
    count=wrapper_f_count(messungen)
    ff,sff=fourier[0],fourier[2]
    fc,sfc=count
    print 'Fourier: {}+-{} ----- zahlen: {}+-{}'.format(ff,sff,fc,sfc)



#messungen=['19,6','28,5','38,9','52,2','68,6','90,0','112,0']
messungen=['19,6','28,5','38,9','52,2','68,6']
data=[]
for string in messungen:
    teilmessungen=[]
    for i in range(5):
        teilmessungen.append(p.lese_lab_datei('lab/'+string+'Ohm/messung'+str(i+1)+'.lab'))
    data.append(teilmessungen)

for teilmessungen in data:
    auswertung(teilmessungen)


#hier plots
#exemplarischer plot: 19,6Ohm Poti:
plt.figure(1)
plt.plot(t1,U1-get_offset(U1))
plt.title('Spannungsverlauf bei 19.6 Ohm am Potentiometer')
plt.xlabel('t[s]')
plt.ylabel('U[V]')
plt.show()

plt.figure(2)
freq1,amp1=p.fourier_fft(t1,U1)
plt.plot(freq1,amp1)
plt.title('Frequenzspektrum bei 19.6 Ohm am Potentiometer')
plt.xlabel('f[Hz]')
plt.ylabel('#')
plt.xlim(0,650)
plt.show()



'''
#debug
U42=U4-get_offset(U4)
plt.figure()
plt.plot(t4,U4)
plt.plot(t4,U42)
plt.axhline(0)
plt.show()
'''
    
    