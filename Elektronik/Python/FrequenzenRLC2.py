# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:19:10 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

#einlesen der werte
messungen=['19,6','28,5','38,9','52,2','68,6']
data=[]
for string in messungen:
    teilmessungen=[]
    for i in range(5):
        teilmessungen.append(p.lese_lab_datei('lab/'+string+'Ohm/messung'+str(i+1)+'.lab'))
    data.append(teilmessungen)




def get_offset(U,start=1800):
    werte=U[start:]
    return np.mean(werte)
    
def get_freq(messung):
    t=messung[:,1]
    U=messung[:,3]
    freq,amp=p.fourier_fft(t,U)
    p.untermenge_daten(freq,amp,0,1000)
    peak=p.peakfinder_schwerpunkt(freq,amp)
#    peak=p.peak(freq,amp,300,500)
    return peak


#peak mittelwerte und fehler und fehler auf mittelwert.
def f_fourier(messungen):
    peaks=[]
#    peakerror=[]
    for x in messungen:
        peaks.append(get_freq(x))
#        peakerror.append(get_freq(x))
    
    mean,std=np.mean(peaks),np.std(peaks,ddof=1)
    mean_error=std/np.sqrt(len(peaks))
#    mean,error=p.gewichtetes_mittel(np.array(peaks),np.array(peakerror))
    
    return mean,std,mean_error
#    return mean,None,error

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

    for i in range(len(times)-1):
        if 2*(times[i+1]-times[i])>0.0024 and 2*(times[i+1]-times[i])<0.0030:
            periods.append(2*(times[i+1]-times[i]))
            error_periods.append(2*np.sqrt(error_times[i+1]**2+error_times[i]**2))

#    output=p.gewichtetes_mittel(np.array(periods),np.array(error_periods))
    
#    plt.figure()
#    plt.plot(t,U)
#    for x in times:
#        plt.axvline(x)
#    plt.show()

#    return(1/output[0],output[1]/output[0]**2)
#    return periods

#der fehler ist VIEEEEEL zu klein, gewichteter mittelwert ist nicht erlaubt!!!!
#dieser output ist erlaubt uind richtig!
    mean=np.mean(np.array(periods))
    std=np.std(np.array(periods),ddof=1)
    return (1/mean,std/mean**2)
#die hier erzeugten werte liegen für alle widerstände innerhalb einer stdabw




def wrapper_f_count(messungen):
    f,sigma_f=[],[]
    for x in messungen:
        f.append(f_count(x[:,1],x[:,3])[0])
        sigma_f.append(f_count(x[:,1],x[:,3])[1])
    
    output=p.gewichtetes_mittel(np.array(f),np.array(sigma_f))
    return output

'''
count=[]
count_err=[]
fourier=[]
fourier_err=[]
    
#    for messungen in data:
for teilversuche in data:
    eins=wrapper_f_count(teilversuche)
    count.append(eins[0])
    count_err.append(eins[1])
    zwei=f_fourier(teilversuche)
    fourier.append(zwei[0])
    fourier_err.append(zwei[1])
    
for j in range(len(count)):
    print 'count={} +- {} ---- fourier={}+-{}'.format(count[i],count_err[i],fourier[i],fourier_err[i])            
'''
       
'''
for x in data:
    liste=[]
    liste2=[]
    for i in range(5):
        liste.append(f_count(x[i][:,1],x[i][:,3])[0])
        liste2.append(f_count(x[i][:,1],x[i][:,3])[1])
    out=p.gewichtetes_mittel(np.array(liste),np.array(liste2))
    print(out[0],'+-',out[1])
'''
'''
for x in data:
    for i in range(5):
        print '\hline'
        print 'x & {} & {} & {}\\\\'.format(np.round(f_count(x[i][:,1],x[i][:,3])[0],2),np.round(f_count(x[i][:,1],x[i][:,3])[1],2),np.round(get_freq(x[i]),2))
'''
for x in data:
    print f_fourier(x)














