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

def daempfung_peaks (datei="19,6", eU_stat=0.002, figure=6):

    sig_U_stat = eU_stat
    sig_t_diff = 0.0001
    delta_peaks = []
    sig_delta_peaks = []
    delta_fit = []
    sig_delta_fit = []
    sig_delta_sys = []
    
    for i in range(5):
        data = p.lese_lab_datei("lab/{:s}Ohm/messung{:1d}.lab".format(datei, i+1))
        t = data[:,1]
        U = data[:,3]
        
        sig_U_sys = 0.01*U + 0.005*10
        
        #offset_U = np.mean(U[-U.size/8:])

        #U = U - offset_U
        
        zeros = get_zeros(t, U, index_output=False)
        peaks = []
        index = []
        
        
        for n in range(len(zeros)-1):
            peaks.append(p.peak(t, U, zeros[n][0], zeros[n+1][0]))
        for peak in peaks:
            indx = find_nearest(t, peak)
            if (np.abs(U[indx]) > 0.05*np.mean(U[0:5])):
                index.append(indx)
        index = np.array(index)
        peaks = []
        
        
        #plt.figure(figure)
        #plt.errorbar(t, U)
        #for x in index:
        #    plt.axvline(t[x])
        
        absU = np.abs(U)
        
        for a in index:
            peaks.append(np.array([t[a], absU[a]]))
        
        
        # Delta direkt ausrechnen
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
        
        
        
        # Delta durch fit ausrechnen
        
        if (index.size>1):                
            
            a, ea, b, eb, chi2, cov = p.lineare_regression(t[index], np.log(absU[index]), sig_U_stat/U[index])
            delta_fit.append(-a)
            sig_delta_fit.append(ea)
            
            if (i == 1 and datei == "28,5"):
                
                # Lin Reg
                plt.figure(20)
                plt.subplot2grid((7,1),(0,0), rowspan=4)
                plt.errorbar(t[index], np.log(absU[index]), sig_U_stat/U[index], fmt = ".")
                plt.plot(t[index], a*t[index]+b)
                plt.ylabel("ln ($U / U_0$) ")
                # Residuen
                plt.subplot2grid((7,1),(-2,0), rowspan=2)
                plt.errorbar(t[index], np.log(absU[index])-a*t[index]-b, yerr=sig_U_stat/U[index], fmt = ".")
                plt.axhline(linestyle="dashed")
                plt.ylabel("Residuen")
                plt.xlabel("t [s]")
                
                
                # Plot Ergebnis
                plt.figure(21)
                plt.plot(t, U)
                plt.xlabel("t (s)")
                plt.ylabel("U (V)")
                
                x = np.arange(0, 0.0205, 0.0005)
                y = np.exp(b)*np.exp(a*x)
                plt.plot(x, y, color="red")
                plt.plot(x, -y, color="red")

            
            # Verschiebemethode
            a1, ea1, b1, eb1, chi2, cov = p.lineare_regression(t[index], np.log(absU[index])-sig_U_sys[index]/absU[index], sig_U_stat/U[index])
            a2, ea2, b2, eb2, chi2, cov = p.lineare_regression(t[index], np.log(absU[index])+sig_U_sys[index]/absU[index], sig_U_stat/U[index])
            
            sig_delta_sys.append((np.abs(a1-a)+np.abs(a2-a))/2)
        
        
        
    if (figure <= 10):
        delta_peaks = np.array(delta_peaks)
        sig_delta_peaks = np.array(sig_delta_peaks)
        
        delta_peaks, sig_delta_peaks = p.gewichtetes_mittel(delta_peaks, sig_delta_peaks)
        
        delta_fit = np.array(delta_fit)
        sig_delta_fit = np.array(sig_delta_fit)
        sig_delta_sys = np.array(sig_delta_sys)
        sig_delta_sys = np.mean(sig_delta_sys)
        delta_fit, sig_delta_fit = p.gewichtetes_mittel(delta_fit, sig_delta_fit)
        
        
        
    return (delta_peaks, sig_delta_peaks, delta_fit, sig_delta_fit, sig_delta_sys)
    


    
Ordnernamen = np.array(["19,6", "28,5", "38,9", "52,2", "68,6", "90,0", "112,0", "130", "140", "150", "200"])

"""
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

"""


# Delta aus Peaks bekommen
delta_peaks = []
sig_delta_peaks = []
delta_fit = []
sig_delta_fit_stat = []
sig_delta_fit_sys = []
for i in range(Ordnernamen.size):
    temp1, temp2, temp3, temp4, temp5 = daempfung_peaks(datei=Ordnernamen[i], figure = 6+i)
    if (temp1):
        delta_peaks.append(temp1)
        sig_delta_peaks.append(temp2)
        delta_fit.append(temp3)
        sig_delta_fit_stat.append(temp4)
        sig_delta_fit_sys.append(temp5)

delta_peaks = np.array(delta_peaks)
sig_delta_peaks = np.array(sig_delta_peaks)

delta = []
sig_delta = []
for i in range(5):
    temp1, temp2 = p.gewichtetes_mittel(np.array([delta_fit[i], delta_peaks[i]]), np.array([sig_delta_fit_sys[i], sig_delta_peaks[i]]))
    delta.append(temp1)
    sig_delta.append(temp2)

delta = np.array(delta)
sig_delta = np.array(sig_delta)

R = np.array([19.6, 28.5, 38.9, 52.2, 68.6])
sig_R_stat = np.full(5, 0.2/np.sqrt(12))

# Fit mit Peaks
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(delta, R, sig_delta, sig_R_stat)
ndof=len(delta)-2

plt.figure(17)
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(delta, R, xerr=sig_delta, yerr=sig_R_stat, fmt=".")
x = np.array([delta[0]*0.90, delta[-1]*1.06])
plt.xlim(x)
y = a*x+b
plt.plot(x, y)
#plt.xlabel("$\delta$ [1/s]")
plt.ylabel("R [$\Omega$]")
plt.figtext(0.15, 0.7, "m = {:2.3f}$\pm${:2.3f}[H]\nb = {:2.2f}$\pm${:2.2f}[$\Omega$]\n$\chi^2$/ndof = {:2.2f}".format(a, ea, b, eb, chi2/ndof))


plt.subplot2grid((6,1),(-2,0), rowspan=2)
y = R-a*delta - b
plt.errorbar(delta, y, yerr = np.sqrt(sig_delta**2* a**2 + sig_R_stat**2), fmt=".")
plt.xlim(x)
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [$\Omega$]")
plt.xlabel("delta [1/s]")


L = 1000*a/2
sig_L = 1000*ea/2

R_rest = -b
sig_R_rest = eb


# Kondensator berechnen
omega = np.array([382.78, 376.84, 373.21, 364.84, 350.75])*2*np.pi
sig_omega = np.array([0.16, 0.18, 0.20, 0.22, 0.24])*2*np.pi

sq_omega = omega**2
sig_sq_omega = 2*omega*sig_omega


sq_delta = delta**2
sig_sq_delta = 2*delta*sig_delta



# Lineare Regression mit Steigung -1 festgelegt
b, eb, chi2 = p.lineare_regression_y_achsenabschnitt_xy(sq_delta, sq_omega, sig_sq_delta, sig_sq_omega)

C = 1000/(b*L)
sig_C=C*np.sqrt( (eb/b)**2 + (sig_L/L)**2 )

# Plot
plt.figure(25)
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(sq_delta, sq_omega, xerr=sig_sq_delta, yerr=sig_sq_omega, fmt=".")
plt.plot(sq_delta, b-sq_delta)
plt.ylabel("$\omega ^2 [1/s^2]$")

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(sq_delta, sq_omega+sq_delta-b, yerr= np.sqrt(sig_sq_delta**2 + sig_sq_omega**2), fmt=".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [$1/s^2$]")
plt.xlabel("$\delta ^2 [1/s^2]$")
plt.figtext(0.55, 0.75, "y = ({:7.0f}$\pm${:5.0f}) $1/s^2$\n $\chi ^2$/ndof = {:1.1f}".format(b, eb, chi2/4))
