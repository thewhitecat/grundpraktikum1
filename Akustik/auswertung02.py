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

messreihe_widerstand = np.array([ widerstand_laufzeitmessung[0:20], widerstand_laufzeitmessung[20:37], np.concatenate((widerstand_laufzeitmessung[37:42], widerstand_laufzeitmessung[43:57])), widerstand_laufzeitmessung[57:77], widerstand_laufzeitmessung[77:97], widerstand_laufzeitmessung[97:116], widerstand_laufzeitmessung[116:136] ])
messreihe_laufzeit = np.array([ laufzeit[0:20], laufzeit[20:37], np.concatenate((laufzeit[37:42], laufzeit[43:57])), laufzeit[57:77], laufzeit[77:97], laufzeit[97:116], laufzeit[116:136] ])

R = np.empty(7)
t=np.empty(7)
sigma_R = np.empty(7)
sigma_t = np.empty(7)




sigma_R = np.empty(7)
sigma_t = np.empty(7)
for i in range(0,7):
    R[i] = np.mean(messreihe_widerstand[i])
    t[i] = np.mean(messreihe_laufzeit[i])
    sigma_R[i] = np.std(messreihe_widerstand[i], ddof=1)
    sigma_t[i] = np.std(messreihe_laufzeit[i], ddof=1)

sigma_R_sys = 0.01


plt.figure(1, [8, 8])
for i in range(1, 5):
    plt.subplot(4, 1, i)
    plt.errorbar(messreihe_laufzeit[i]*1000, messreihe_widerstand[i], xerr=sigma_t[i]*1000, yerr=sigma_R[i]+sigma_R_sys, fmt=".")
    plt.ylabel("R / $k\Omega$")
    plt.xlabel("t / $ms$")




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
plt.errorbar(widerstand, strecke, yerr=0.03+0.07/np.sqrt(3), xerr=sigma_R, fmt="k.")



a, ea, b, eb, chi2, cov = p.lineare_regression_xy(widerstand, strecke, sigma_R, np.full(7, 0.015+0.07/np.sqrt(3)))

cm_pro_kOhm = np.abs(a)
sigma_cm_pro_kOHm = ea

# Plot Fit
x=np.arange(10)*2.5/10 +0.3
y=a*x+b
plt.plot(x, y)
dof = widerstand.size -2
plt.figtext(0.55, 0.71, "$\Delta s = {:2.2f}(cm/k\Omega)*\Delta R$\n$\sigma_k={:1.2f}cm / k\Omega$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/dof))










# Array für Lin Reg
sigma_R_array = np.concatenate( (np.full(20, sigma_R[0]), np.full(17, sigma_R[1]), np.full(20, sigma_R[2]), np.full(20, sigma_R[3]), np.full(20, sigma_R[4]), np.full(19, sigma_R[5]), np.full(20, sigma_R[5])) )
sigma_t_array = np.concatenate( (np.full(20, sigma_t[0]), np.full(17, sigma_t[1]), np.full(20, sigma_t[2]), np.full(20, sigma_t[3]), np.full(20, sigma_t[4]), np.full(19, sigma_t[5]), np.full(20, sigma_t[5])) )



# Plot Laufzeitmessung Rohdaten
plt.figure(4)
plt.subplot(1,1,1)
#plt.errorbar(laufzeit, widerstand_laufzeitmessung, xerr=np.ones(laufzeit.size)*np.mean(sigma_t), yerr= np.ones(laufzeit.size)*np.mean(sigma_R), fmt="k.")
plt.errorbar(t, R, xerr=sigma_t, yerr= sigma_R+sigma_R_sys, fmt="k.")
plt.title("Laufzeitmessung")
plt.xlabel("Laufzeit / s")
plt.ylabel("Widerstand / kOhm")

# Linreg Laufzeitmessung
#a, ea, b, eb, chi2, cov = p.lineare_regression_xy(laufzeit, widerstand_laufzeitmessung, sigma_t_array, sigma_R_array)
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(t, R, sigma_t/4.3, (sigma_R)/4.3+sigma_R_sys)


# Plot Fit
x=np.arange(10)*0.001/9+0.00065
y=a*x+b
plt.plot(x, y)
dof = t.size -2
plt.figtext(0.15, 0.70, "$\Delta R / \Delta t = {:2.2f}(k\Omega /s)$\n$\sigma_a={:1.2f}k\Omega / s$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/dof))

# Pullverteilung
plt.figure(5)

plt.subplot(2, 1, 1)
plt.errorbar(laufzeit, widerstand_laufzeitmessung - laufzeit*a-b, fmt=".")
plt.title("Residuen- und Pullverteilung")
plt.subplot(2, 1, 2)
plt.hist(widerstand_laufzeitmessung - laufzeit*a-b, bins =15)


# Schgallgeschwindigkeit berechnen
v_laufzeitmessung = cm_pro_kOhm * a/100
sigma_sys_v_laufzeitmessung = v_laufzeitmessung * (sigma_cm_pro_kOHm/cm_pro_kOhm)
sigma_stat_v_laufzeitmessung = v_laufzeitmessung * ea/a
sigma_v_laufzeitmessung = sigma_stat_v_laufzeitmessung+sigma_sys_v_laufzeitmessung
print("Laufzeitmessung ergibt:\n v={:4.4f}m/s \n sigma _v = {:2.4f}m/s".format(v_laufzeitmessung, sigma_v_laufzeitmessung))