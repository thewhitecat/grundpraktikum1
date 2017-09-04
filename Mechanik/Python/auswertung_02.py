# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:00:06 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

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

def get_peaks(x, y):
    zeros = get_zeros(x, y, index_output=False)
    peaks = []
    index = []
    
    for n in range(len(zeros)-1):
        #temp1, temp2 = peak_fehler(x, y, zeros[2], zeros[n+1][2])
        #peaks.append(temp1)
        #peaks.append(temp2)
        peaks.append(p.peak(x, y, zeros[n][0], zeros[n+1][0]))
    for peak in peaks:
        indx = find_nearest(x, peak)
        if (np.abs(y[indx]) > 0.02*np.mean(np.abs(y[0])) and x[indx] > 0.1):
            index.append(indx)
    index = np.array(index)
    
    return index#, sigma
    
def get_peaks_fehler(x, y):
    zeros = get_zeros(x, y, index_output=False)
    peaks = []
    sigma = []
    index = []
    
    for n in range(len(zeros)-1):
        temp1, temp2 = peak_fehler(x, y, zeros[n][2], zeros[n+1][2])
        peaks.append(temp1)
        sigma.append(temp2)
    for peak in peaks:
        indx = find_nearest(x, peak)
        if (np.abs(y[indx]) > 0.02*np.mean(np.abs(y[0])) and x[indx] > 0.1):
            index.append(indx)
    index = np.array(index)
    
    return index, sigma

def peak_fehler(x, y, i0, i1):
    peaks = []
    #i0 = np.array(i0)
    #i1 = np.array(i1)
    abweichungen = (i1-i0)/20
    peaks.append( p.peakfinder_schwerpunkt(x[i0:i1], y[i0:i1]) )
    for i in range(1, 10):
        peaks.append( p.peakfinder_schwerpunkt(x[i0+i*abweichungen:i1], y[i0+i*abweichungen:i1]) )
        peaks.append( p.peakfinder_schwerpunkt(x[i0:i1-i*abweichungen], y[i0:i1-i*abweichungen]) )
        peaks.append( p.peakfinder_schwerpunkt(x[i0+i*abweichungen:i1-i*abweichungen], y[i0+i*abweichungen:i1-i*abweichungen]) )
    peaks = np.array(peaks)
    peak = np.mean(peaks)
    sig_peak = np.std(peaks, ddof =1)/peaks.size
    
    return peak, sig_peak

def daempfung(t, U, index, i=20):
    absU = np.abs(U)
    sig_U_stat = np.std(U[-3*U.size/4:], ddof=1)
    a, ea, b, eb, chi2, cov = p.lineare_regression(t[index], np.log(absU[index]), sig_U_stat/U[index])
    delta = (-a)
    sig_delta_stat = ea
    
    sig_U_sys = 0.01*U + 0.005*1
    if i == i:    
        # Lin Reg
        plt.figure(2*i)
        plt.subplot2grid((7,1),(0,0), rowspan=4)
        plt.errorbar(t[index], np.log(absU[index]), sig_U_stat/U[index], fmt = ".")
        plt.plot(t[index], a*t[index]+b)
        plt.ylabel("ln ($U / U_0$) ")
        ndof = index.size-2
        plt.figtext(0.2, 0.2, "m = {:3.2f} $\pm$ {:3.2f} 1/s\n b = {:2.3f} $\pm$ {:2.3f} \n $\chi^2$/ndof = {:3.4f}".format(a, ea, b, eb, chi2/ndof))
        # Residuen
        plt.subplot2grid((7,1),(-2,0), rowspan=2)
        plt.errorbar(t[index], np.log(absU[index])-a*t[index]-b, yerr=sig_U_stat/U[index], fmt = ".")
        plt.axhline(linestyle="dashed")
        plt.ylabel("Residuen")
        plt.xlabel("t [s]")
        
        
        # Plot Ergebnis
        plt.figure(2*i+1)
        plt.plot(t, U)
        plt.xlabel("t (s)")
        plt.ylabel("U (V)")
        
        x = np.arange(0, 25, 0.5)
        y = np.exp(b)*np.exp(a*x)
        plt.plot(x, y, color="red")
        plt.plot(x, -y, color="red")
    
    
    # Verschiebemethode
    a1, ea1, b1, eb1, chi2, cov = p.lineare_regression(t[index], np.log(absU[index])-sig_U_sys[index]/absU[index], sig_U_stat/U[index])
    a2, ea2, b2, eb2, chi2, cov = p.lineare_regression(t[index], np.log(absU[index])+sig_U_sys[index]/absU[index], sig_U_stat/U[index])
    
    sig_delta_sys = ((np.abs(a1-a)+np.abs(a2-a))/2)
    return (delta, sig_delta_stat, sig_delta_sys)


def periodendauer_mitte(feder=2, ordner="Stab_mitte"):
    t0 = []
    t1 = []
    index_lenght=15
    for i in range(5):
        data = p.lese_lab_datei("lab/Feder{:1d}/{:s}/messung{:1d}.lab".format(feder, ordner, i+1))
        t = data[:,1]
        U = data[:,2]
        
        U, t = p.untermenge_daten(U, t, -1, 1)
        
        U = U - np.mean(U[-U.size/5:])
        
        indizes = get_peaks(t, U)
        
        if indizes.size > index_lenght:
            indizes = indizes[:index_lenght]
        print indizes.size
        
        #daempfung(t, U, indizes, i)
        
        plt.figure(1)
        plt.errorbar(t[indizes], U[indizes], fmt=".")
        
        t0.append(t[indizes[0]])
        t1.append(t[indizes[-1]])
        
    t0 = np.array(t0)
    t1 = np.array(t1)
    
    sig_t0 = np.std(t0, ddof=1)/np.sqrt(t0.size) 
    sig_t1 = np.std(t1, ddof=1)/np.sqrt(t1.size)
    
    t0 = np.mean(t0)
    t1 = np.mean(t1)
    
    T = 2*(t1-t0)/(indizes.size-1)
    sig_T = 2*np.sqrt(sig_t0**2+sig_t1**2)/(indizes.size-1)
    print sig_T
    print sig_t0, sig_t1
    return T, sig_T

def periodendauer(datei):
    t0 = []
    t1 = []
    index_lenght=12
    
    data = p.lese_lab_datei(datei)
    t = data[:,1]
    U = data[:,2]
    
    U, t = p.untermenge_daten(U, t, -2, 2)
    
    U = U - np.mean(U[-U.size/6:])
    
    indizes, sigma = get_peaks_fehler(t, U)
    
    if indizes.size > index_lenght:
        indizes = indizes[:index_lenght]
        sigma = sigma[:index_lenght]
    print indizes.size
    
    #daempfung(t, U, indizes, i)
    
    
    t0.append(t[indizes[0]])
    t1.append(t[indizes[-1]])
    
    t0 = np.array(t0)
    t1 = np.array(t1)
    
    t0 = np.mean(t0)
    t1 = np.mean(t1)
    
    T = 2*(t1-t0)/(indizes.size-1)
    sig_T = 2*np.sqrt(sigma[0]**2 + sigma[-1]**2)/(indizes.size-1)
    return T, sig_T

def periodendauer_linreg (datei):
    
    sig_t = 0.011/np.sqrt(2)
    
    data = p.lese_lab_datei(datei)
    
    t = data[:,1]
    U = data[:,2]
    
    U, t = p.untermenge_daten(U, t, -2, 2)
    
    index = get_peaks(t, U)
    
    anzahl = index.size/2
    if anzahl*2 < index.size:
        anzahl = anzahl + 0.5
    n = np.arange(0, anzahl, 0.5)
    a, ea, b, eb, chi2, cov = p.lineare_regression(n, t[index], np.full(index.size,sig_t))
    
    return (a, ea)
    
    
    
    
    
def auswertung_D (feder=2):
    T = []
    sig_T = []
    temp1, temp2 = periodendauer_mitte(2, "Stab_mitte")
    T.append(temp1)
    sig_T.append(temp2)
    print sig_T
    
    temp1, temp2 = periodendauer("lab/Feder2/Stab_Massen/Aussen_01.lab")
    T.append(temp1)
    sig_T.append(temp2)
    
    for i in range(1,6):
        
        datei = "lab/Feder2/Stab_Massen/Aussen-{:1d}.lab".format(i)
        temp1, temp2 = periodendauer(datei)
        T.append(temp1)
        sig_T.append(temp2)
        
    print sig_T
    print T
    T=np.array(T)
    
    T_sq = T**2
    sig_T_sq = 2*T*sig_T
    
    R = np.concatenate((np.array([0.0]),0.05*np.array([6, 5, 4, 3, 2, 1])))
    sig_R = 0.001/np.sqrt(12)
    sig_R_sys = 0.0007
    
    R_sq = R**2
    sig_R_sq = 2*R*sig_R*np.sqrt(np.array([0,6,5,4,3,2,1]))
    sig_R_sq_sys = sig_R_sys * 2 * np.sqrt(np.sqrt([0,6,5,4,3,2,1])) * R
    sig_R_sq[0] = 1e-6
    m_Massen = 0.476
    sig_m_stat = 0.0001/np.sqrt(12)
    sig_m_sys = 0.0002
    
    a, ea, b, eb, chi2, cov = p.lineare_regression_xy(R_sq, T_sq, sig_R_sq, sig_T_sq)
    # Lin Reg
    plt.figure(3, [8,8])
    plt.subplot2grid((6,1),(0,0), rowspan=4)
    plt.errorbar(R_sq, T_sq, xerr=sig_R_sq, yerr=sig_T_sq, fmt = ".")
    plt.plot(R_sq, a*R_sq+b)
    plt.ylabel("$T^2 [s^2]$")
    ndof = R_sq.size-2
    plt.figtext(0.2, 0.7, "m = {:3.2f} $\pm$ {:3.2f} $s^2/m^2$\n b = {:2.3f} $\pm$ {:2.3f} $s^2$ \n $\chi^2$/ndof = {:3.3f}".format(a, ea, b, eb, chi2/ndof))
    # Residuen
    plt.subplot2grid((6,1),(-2,0), rowspan=2)
    plt.errorbar(R_sq, T_sq-a*R_sq-b, yerr=np.sqrt(sig_T_sq**2+a**2*sig_R_sq**2), fmt = ".")
    plt.axhline(linestyle="dashed")
    plt.ylabel("Residuen [$s^2$]")
    plt.xlabel("$r^2$ [$m^2$]")
    
    
    # Verschiebemethode, wegen sys Fehler auf R
    a1, ea1, b1, eb1, chi21, cov1 = p.lineare_regression_xy(R_sq-sig_R_sq_sys, T_sq, sig_R_sq, sig_T_sq)
    a2, ea2, b2, eb2, chi22, cov2 = p.lineare_regression_xy(R_sq+sig_R_sq_sys, T_sq, sig_R_sq, sig_T_sq)
    
    sig_a_sys = (np.abs(a1-a) + np.abs(a2-a))/2
    sig_b_sys = (np.abs(b1-b) + np.abs(b2-b))/2
    
    print a, ea, sig_a_sys            
                
    D = 4*np.pi**2*m_Massen/a
    sig_D = D* np.sqrt((sig_m_stat/m_Massen)**2 + (ea/a)**2)
    sig_D_sys = D*np.sqrt((sig_m_sys/m_Massen)**2 + (sig_a_sys/a)**2)
    sig_D_sys_ohne_M = D*np.sqrt((sig_a_sys/a)**2)
    J_stab = b*D/(4*np.pi**2)
    sig_J_stab_stat = J_stab*np.sqrt( (eb/b)**2 + (sig_D/D)**2 )
    sig_J_stab_sys = J_stab*np.sqrt( (sig_D_sys/D)**2 + (sig_b_sys/b)**2 )
    
    return D, sig_D, sig_D_sys, J_stab, sig_J_stab_stat, sig_J_stab_sys



#T, sig_T = periodendauer_linreg("lab/Feder2/Stab_Massen/Aussen-{:1d}.lab".format(i))


D, sig_D_stat, sig_D_sys, J_stab, sig_J_stab_stat, sig_J_stab_sys = auswertung_D()