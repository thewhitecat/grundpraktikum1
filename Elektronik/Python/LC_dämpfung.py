# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:42:52 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def daempfung_fit (datei="19,6", eU_stat=0.001496, figure=1):
    U = np.empty((5,2001))
    t = np.empty((5, 2001))
    sig_U_stat = eU_stat
    
    
    
    A0 = np.empty(5)
    sig_A0 = np.empty(5)
    delta = np.empty(5)
    sig_delta = np.empty(5)
    
    peak_t = []
    peak_U = []
    peak_U_Fehler = []
    
    for i in range(5):
        data = p.lese_lab_datei("lab/{:s}Ohm/messung{:1d}.lab".format(datei, i+1))
        t[i] = data[:,1]
        U[i] = data[:,3]
        
        #offset_U = np.mean(U[i][-U[i].size/8:])
        #U[i] = U[i] - offset_U
        
        A0[i], sig_A0[i], delta[i], sig_delta[i], GutePeaks, GutePeakZeiten, GutePeakFehler = \
          p.exp_einhuellende(t[i], U[i], np.full(U[i].size, sig_U_stat), Sens=0.05)
        
        peak_t.append(GutePeakZeiten)
        peak_U.append(GutePeaks)
        peak_U_Fehler.append(GutePeakFehler)
        
        if (i == 1):
            plt.figure(figure)
            plt.plot(t[i], U[i])
            plt.xlabel("t (s)")
            plt.ylabel("U (V)")
            
            
            x = np.arange(0, 0.02, 0.0005)
            y = A0[i]*np.exp(-delta[i]*x)
            plt.plot(x, y)
            plt.plot(x, -y)
    
    
    
    mean_delta, sig_mean_delta = p.gewichtetes_mittel(delta, sig_delta)
    
    return (mean_delta, sig_mean_delta)
 
def get_zeros(t,U,index_output=True):
    '''
    gibt liste mit Tupeln der Form (t,U,index) zurück,
    dieser index und nächster sind die "nullstellen"
    '''
    zeros=[]
    for i in range(len(U)-1):
        if U[i]>0 and U[i+1]<0:
            zeros.append((t[i],U[i],i))
        elif U[i]<0 and U[i+1]>0:
            zeros.append((t[i],U[i],i))
        elif U[i]==0 and U[i-1] and i>0:
            zeros.append((t[i],U[i],i))
    #don't bother with this stuff
    if index_output==False:
        return zeros
    else:
        index=[]
        for x in zeros:
            index.append((x[2],x[2]+1))
        return index    

def daempfung_peaks (datei="19,6", eU_stat=0.001496, figure=6):

    sig_U_stat = eU_stat
    sig_t_diff = 0.0001
    delta_peaks = []
    sig_delta_peaks = []
    for i in range(5):
        data = p.lese_lab_datei("lab/{:s}Ohm/messung{:1d}.lab".format(datei, i+1))
        t = data[:,1]
        U = data[:,3]
        
        #offset_U = np.mean(U[-U.size/8:])

        #U = U - offset_U
        
        zeros = get_zeros(t, U, index_output=False)
        peaks = []
        index = []
        
        
        for i in range(len(zeros)-1):
            peaks.append(p.peak(t, U, zeros[i][0], zeros[i+1][0]))
        for peak in peaks:
            indx = find_nearest(t, peak)
            if (np.abs(U[indx]) > 0.05*np.mean(U[0:5])):
                index.append(indx)
        
        peaks = []
        
        
        plt.figure(figure)
        plt.errorbar(t, U)
        for x in index:
            plt.axvline(t[x])
        
        U = np.abs(U)
        
        for a in index:
            peaks.append(np.array([t[a], U[a]]))
        
        
        
        delta_peaks_temp = []
        sig_delta_temp = []
        for x in range(len(peaks)-1):
            y = peaks[x][1]/peaks[x+1][1]
            diff_t = (peaks[x+1][0]-peaks[x][0])
            delta_peaks_temp.append( np.log(y) /diff_t )
            sig_delta_temp.append(delta_peaks_temp[-1] * np.sqrt( sig_U_stat**2 *( (1/peaks[x][1]+1/peaks[x+1][1])/(y*np.log(y)))**2 + sig_t_diff**2/diff_t**2 ))
        
        delta_peaks_temp = np.array(delta_peaks_temp)
        sig_delta_temp = np.array(sig_delta_temp)
        if (figure <= 10):
            delta_peaks_temp, sig_delta_temp = p.gewichtetes_mittel(delta_peaks_temp, sig_delta_temp)
            
            delta_peaks.append(delta_peaks_temp)
            sig_delta_peaks.append(sig_delta_temp)
    
    if (figure <= 10):
        delta_peaks = np.array(delta_peaks)
        sig_delta_peaks = np.array(sig_delta_peaks)
        
        delta_peaks, sig_delta_peaks = p.gewichtetes_mittel(delta_peaks, sig_delta_peaks)
        
    return (delta_peaks, sig_delta_peaks)
    


    
Ordnernamen = np.array(["19,6", "28,5", "38,9", "52,2", "68,6", "90,0", "112,0", "130", "140", "150", "200"])

# Delta aus fit bekommen
delta_fit = np.empty(4)
sig_delta_fit = np.empty(4)
for i in range(4):
    delta_fit[i], sig_delta_fit[i] = daempfung_fit(datei=Ordnernamen[i], figure=i+1)

R = np.array([19.6, 28.5, 38.9, 52.2])
sig_R_stat = np.full(4, 0.2/np.sqrt(12))

# Fit deltas benutzen, um L und Restwiderstand zu berechnen

a, ea, b, eb, chi2, cov = p.lineare_regression_xy(delta_fit, R, sig_delta_fit, sig_R_stat)


plt.figure(5)
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(delta_fit, R, xerr=sig_delta_fit, yerr=sig_R_stat, fmt=".")
x = np.array([delta_fit[0]*0.90, delta_fit[-1]*1.06])
plt.xlim(x)
y = a*x+b
plt.plot(x, y)
#plt.xlabel("$\delta$ [1/s]")
plt.ylabel("R [$\Omega$]")


plt.subplot2grid((6,1),(-2,0), rowspan=2)
y = R-a*delta_fit - b
plt.errorbar(delta_fit, y, yerr = np.sqrt(sig_delta_fit**2 + a**2*sig_R_stat**2), fmt=".")
plt.xlim(x)
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("delta [1/s]")


L_fit = 1000*a/2
sig_L_fit = 1000*ea/2

R_rest_fit = -b
sig_R_rest_fit = eb




# Delta aus Peaks bekommen
delta_peaks = []
sig_delta_peaks = []
for i in range(Ordnernamen.size):
    temp1, temp2 = daempfung_peaks(datei=Ordnernamen[i], figure = 6+i)
    if (temp1):
        delta_peaks.append(temp1)
        sig_delta_peaks.append(temp2)

delta_peaks = np.array(delta_peaks)
sig_delta_peaks = np.array(sig_delta_peaks)


R = np.array([19.6, 28.5, 38.9, 52.2, 68.6])
sig_R_stat = np.full(5, 0.2/np.sqrt(12))

# Fit mit Peaks
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(delta_peaks, R, sig_delta_peaks, sig_R_stat)


plt.figure(16)
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(delta_peaks, R, xerr=sig_delta_peaks, yerr=sig_R_stat, fmt=".")
x = np.array([delta_peaks[0]*0.90, delta_peaks[-1]*1.06])
plt.xlim(x)
y = a*x+b
plt.plot(x, y)
#plt.xlabel("$\delta$ [1/s]")
plt.ylabel("R [$\Omega$]")


plt.subplot2grid((6,1),(-2,0), rowspan=2)
y = R-a*delta_peaks - b
plt.errorbar(delta_peaks, y, yerr = np.sqrt(sig_delta_peaks**2 + a**2*sig_R_stat**2), fmt=".")
plt.xlim(x)
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("delta [1/s]")


L_peaks = 1000*a/2
sig_L_peaks = 1000*ea/2

R_rest_peaks = -b
sig_R_rest_peaks = eb