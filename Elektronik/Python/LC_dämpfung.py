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

def daempfung (datei="19,6", eU_stat=0.004, figure=6):

    sig_U_stat = eU_stat
    sig_t_diff = 0.0001
    delta_peaks = []
    sig_delta_peaks = []
    delta_fit = []
    sig_delta_fit_stat = []
    sig_delta_fit_sys = []
    
    # Alle 5 Messungen zu einem Widerstand durchgehen
    for i in range(5):
        data = p.lese_lab_datei("lab/{:s}Ohm/messung{:1d}.lab".format(datei, i+1))
        t = data[:,1]
        U = data[:,3]
        
        
        sig_U_sys = 0.01*U + 0.005*10
        
        
        zeros = get_zeros(t, U, index_output=False)
        peaks = []
        index = []
        
        
        for n in range(len(zeros)-1):
            peaks.append(p.peak(t, U, zeros[n][0], zeros[n+1][0]))
        for peak in peaks:
            indx = find_nearest(t, peak)
            if (np.abs(U[indx]) > 0.03*np.mean(U[0:5])):
                index.append(indx)
        index = np.array(index)
        peaks = []
        
        # Offset korrigieren
        offset_U = np.mean(U[-U.size/8:])
        U = U - offset_U
        
        # Betrag der Spannung für Amplitudenbestimmung
        absU = np.abs(U)
        
        
        # peaks[i] liefert t und absU des i-ten Peaks
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
            sig_delta_fit_stat.append(ea)
            
            if (i == 2 and datei == "19,6"):
                
                # Lin Reg
                plt.figure(20)
                plt.subplot2grid((7,1),(0,0), rowspan=4)
                plt.errorbar(t[index], np.log(absU[index]), sig_U_stat/U[index], fmt = ".")
                plt.plot(t[index], a*t[index]+b)
                plt.ylabel("ln ($U / U_0$) ")
                ndof = index.size-2
                plt.figtext(0.6, 0.7, "m = {:3.2f} $\pm$ {:3.2f} 1/s\n b = {:2.3f} $\pm$ {:2.3f} \n $\chi^2$/ndof = {:3.1f}".format(a, ea, b, eb, chi2/ndof))
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
            
            sig_delta_fit_sys.append((np.abs(a1-a)+np.abs(a2-a))/2)
        
        
        
    if (index.size>1):
        delta_peaks = np.array(delta_peaks)
        sig_delta_peaks = np.array(sig_delta_peaks)
        
        
        
        delta_fit = np.array(delta_fit)
        sig_delta_fit_stat = np.array(sig_delta_fit_stat)
        sig_delta_fit_sys = np.array(sig_delta_fit_sys)
        
        print("Widerstand {:s}".format(datei))
        for i in range(len(delta_peaks)):
            print("{:1d} & {:4.1f} $\pm$ {:2.1f} & {:4.1f} $\pm$ {:2.1f} $\pm$ {:2.1f}".format(i+1, delta_peaks[i], sig_delta_peaks[i], delta_fit[i], sig_delta_fit_stat[i], sig_delta_fit_sys[i]))
        #sig_delta_fit_sys = np.mean(sig_delta_fit_sys)
        #delta_peaks, sig_delta_peaks = p.gewichtetes_mittel(delta_peaks, sig_delta_peaks)
        #delta_fit, sig_delta_fit_stat = p.gewichtetes_mittel(delta_fit, sig_delta_fit_stat)
        if (datei == "19,6"):
            delta2, sig_delta2 = p.gewichtetes_mittel (delta_fit[:-1], sig_delta_fit_stat[:-1])
        else:
            delta2, sig_delta2 = p.gewichtetes_mittel (delta_fit, sig_delta_fit_stat)
        delta1, sig_delta1 = p.gewichtetes_mittel (delta_peaks, sig_delta_peaks)
        
        delta, sig_delta = p.gewichtetes_mittel(np.array([delta1, delta2]), np.array([sig_delta1, sig_delta2]))
        
        
        
        print(delta1, delta2)
        print (delta, sig_delta)
        #return (delta_peaks, sig_delta_peaks, delta_fit, sig_delta_fit_stat, sig_delta_fit_sys)
        return (delta, sig_delta)
    else:
        return (None, None)
        
        
    
    


    
Ordnernamen = np.array(["19,6", "28,5", "38,9", "52,2", "68,6", "90,0", "112,0", "130", "140", "150", "200"])




# Delta bekommen
delta_peaks = []
sig_delta_peaks = []
delta_fit = []
sig_delta_fit_stat = []
sig_delta_fit_sys = []


delta = []
sig_delta = []
for i in range(Ordnernamen.size):
    temp1, temp2 = daempfung(datei=Ordnernamen[i], figure = 6+i)
    if (temp1):
        #delta_peaks.append(temp1)
        #sig_delta_peaks.append(temp2)
        #delta_fit.append(temp3)
        #sig_delta_fit_stat.append(temp4)
        #sig_delta_fit_sys.append(temp5)
        
        delta.append(temp1)
        sig_delta.append(temp2)

#delta_peaks = np.array(delta_peaks)
#sig_delta_peaks = np.array(sig_delta_peaks)
#
#delta = []
#sig_delta = []
#for i in range(5):
#    temp1, temp2 = p.gewichtetes_mittel(np.array([delta_fit[i], delta_peaks[i]]), np.array([sig_delta_fit_sys[i], sig_delta_peaks[i]]))
#    delta.append(temp1)
#    sig_delta.append(temp2)
#
delta = np.array(delta)
sig_delta = np.array(sig_delta)


R = np.array([19.6, 28.5, 38.9, 52.2, 68.6])
sig_R_stat = np.full(5, 0.2/np.sqrt(12))

# Lin Reg für L und R
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

# Residuen
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
omega = np.array([381.85, 377.29, 373.66, 363.64, 349.12])*2*np.pi
sig_omega = np.array([2.15, 4.90, 3.4, 2.63, 4.15])*2*np.pi

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
plt.figtext(0.55, 0.75, "y = ({:7.0f}$\pm${:5.0f}) $1/s^2$\n $\chi ^2$/ndof = {:1.2f}".format(b, eb, chi2/4))
