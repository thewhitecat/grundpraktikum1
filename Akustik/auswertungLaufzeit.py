# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 14:52:00 2017

@author: Sebastian
"""

import Praktikum as p
import pylab as pyl
import numpy as np
import matplotlib.pyplot as plt


"""
Laufzeitmessungen
"""


laufzeitmessung = p.lese_lab_datei("cassy\Laufzeit.lab")

laufzeit = laufzeitmessung[:,2]
widerstand_laufzeitmessung = laufzeitmessung[:,3]

"""
Rauschberechnung
"""

messreihe_widerstand = np.array([ widerstand_laufzeitmessung[0:20], widerstand_laufzeitmessung[20:37], widerstand_laufzeitmessung[37:57], widerstand_laufzeitmessung[57:77], widerstand_laufzeitmessung[77:97], widerstand_laufzeitmessung[97:116], widerstand_laufzeitmessung[116:136] ])
messreihe_laufzeit = np.array([ laufzeit[0:20], laufzeit[20:37], laufzeit[37:457], laufzeit[57:77], laufzeit[77:97], laufzeit[97:116], laufzeit[116:136] ])

R = np.empty(7)
t=np.empty(7)
sigma_R = np.empty(7)
sigma_t = np.empty(7)




sigma_R = np.empty(7)
sigma_t = np.empty(7)
for i in range(0,7):
    R[i] = np.mean(messreihe_widerstand[i])
    t[i] = np.mean(messreihe_laufzeit[i])
    sigma_R[i] = np.std(messreihe_widerstand[i], ddof=1)+10/(4096*np.sqrt(12))#/np.sqrt(messreihe_widerstand[i].size)
    sigma_t[i] = np.std(messreihe_laufzeit[i], ddof=1)#/np.sqrt(messreihe_widerstand[i].size)

sigma_R_sys = 0.01


#plt.figure(1, [8, 8])
#for i in range(1, 5):
 #   plt.subplot(4, 1, i)
  #  plt.errorbar(messreihe_laufzeit[i]*1000, messreihe_widerstand[i], fmt=".")
   # plt.ylabel("R / $k\Omega$")
    #plt.xlabel("t / $ms$")




"""
Kalibrieren des Potentiometers zur Längenmessung
"""

kalibrierung = p.lese_lab_datei("cassy\Kalibrierung.lab")

widerstand = kalibrierung[:,2]
strecke = kalibrierung[:,3]

# Plot Rohdaten
plt.figure(2, [10,10])
plt.errorbar(laufzeit*1000, widerstand_laufzeitmessung, fmt="k.")
plt.ylabel("Widerstand / $k\Omega$")
plt.xlabel("Laufzeit / ms")


# Plot mit Fit
plt.figure(3)
plt.subplot(1, 1, 1)
plt.title("Messdaten zur Kalibration mit Fit")
plt.ylabel("Strecke / cm")
plt.xlabel("Widerstand / kOhm")
plt.errorbar(widerstand, strecke, yerr=0.03+0.07/np.sqrt(3), xerr=sigma_R+sigma_R_sys, fmt="k.")



a, ea, b, eb, chi2, cov = p.lineare_regression_xy(widerstand, strecke, sigma_R+sigma_R_sys, np.full(7, 0.015+0.07/np.sqrt(3)))

cm_pro_kOhm = 15.99#np.abs(a)
sigma_cm_pro_kOHm = 0.07#ea

# Plot Fit
x=np.arange(2)*1.9 +0.5
y=a*x+b
plt.plot(x, y)
dof = widerstand.size -2
plt.figtext(0.55, 0.71, "$\Delta s = {:2.2f}(cm/k\Omega)*\Delta R$\n$\sigma_k={:1.2f}cm / k\Omega$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/dof))


# Plot Residuen
plt.figure(4)
plt.subplot(2, 1, 1)
plt.errorbar(widerstand, (strecke - widerstand*a-b), xerr=sigma_R+sigma_R_sys, yerr=0.03+0.07/np.sqrt(3), fmt=".")
plt.title("Residuenverteilung")






# Array für Lin Reg
sigma_R_array = sigma_R_sys + np.concatenate( (np.full(20, sigma_R[0]), np.full(17, sigma_R[1]), np.full(20, sigma_R[2]), np.full(20, sigma_R[3]), np.full(20, sigma_R[4]), np.full(19, sigma_R[5]), np.full(20, sigma_R[5])) )
sigma_t_array = np.concatenate( (np.full(20, sigma_t[0]), np.full(17, sigma_t[1]), np.full(20, sigma_t[2]), np.full(20, sigma_t[3]), np.full(20, sigma_t[4]), np.full(19, sigma_t[5]), np.full(20, sigma_t[5])) )



# Plot Laufzeitmessung Rohdaten
plt.figure(5)
plt.subplot(1, 1, 1)
plt.errorbar(laufzeit, widerstand_laufzeitmessung, xerr=sigma_t_array, yerr= sigma_R_array, fmt="k.")
#plt.errorbar(t, R, xerr=sigma_t, yerr= sigma_R, fmt="k.")
plt.title("Laufzeitmessung")
plt.xlabel("Laufzeit / s")
plt.ylabel("Widerstand / $k\Omega$")

# Linreg Laufzeitmessung
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(laufzeit, widerstand_laufzeitmessung, sigma_t_array, sigma_R_array)
#a, ea, b, eb, chi2, cov = p.lineare_regression_xy(t[0:5], R[0:5], sigma_t[0:5], sigma_R[0:5])
print (a)
print (ea)
print (b)
print (eb)
print (chi2/5)

# Plot Fit
x=np.arange(9)*0.001/9+0.0007
y=a*x+b
plt.plot(x, y)
dof = t.size -2
plt.figtext(0.15, 0.70, "$\Delta R / \Delta t = {:2.2f}(k\Omega /s)$\n$\sigma_a={:1.2f}k\Omega / s$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/dof))

# Residuenverteilung
sigma_residuen = np.empty(sigma_R_array.size)
for i in range(sigma_R_array.size):
    sigma_residuen[i] = np.sqrt(sigma_R_array[i]**2+a**2*sigma_t_array[i]**2)
    
plt.figure(6)
plt.subplot(2, 1, 1)
#plt.plot(t, np.zeros(7))
plt.axhline(ls="dashed")
plt.errorbar(laufzeit, (widerstand_laufzeitmessung - laufzeit*a-b), yerr=sigma_residuen, fmt="k.")
plt.ylabel("Residuen / $k\Omega$")
plt.xlabel("t / s")
plt.title("Residuenverteilung")


# Schgallgeschwindigkeit berechnen
v_laufzeitmessung = cm_pro_kOhm * a/100
sigma_sys_v_laufzeitmessung = v_laufzeitmessung * (sigma_cm_pro_kOHm/cm_pro_kOhm)
sigma_stat_v_laufzeitmessung = v_laufzeitmessung * ea/a
sigma_v_laufzeitmessung = np.sqrt(sigma_stat_v_laufzeitmessung**2+sigma_sys_v_laufzeitmessung**2)
print("Laufzeitmessung ergibt:\n v={:4.4f}m/s \n sigma _v = {:2.4f}m/s".format(v_laufzeitmessung, sigma_v_laufzeitmessung))