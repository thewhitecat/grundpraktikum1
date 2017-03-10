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
R = np.empty(7)
t=np.empty(7)
sigma_R = np.empty(7)
sigma_t = np.empty(7)
R[0] = np.mean(widerstand_laufzeitmessung[0:20])
R[1] = np.mean(widerstand_laufzeitmessung[20:37])
R[2] = np.mean(widerstand_laufzeitmessung[37:57])
R[3] = np.mean(widerstand_laufzeitmessung[57:77])
R[4] = np.mean(widerstand_laufzeitmessung[77:97])
R[5] = np.mean(widerstand_laufzeitmessung[97:116])
R[6] = np.mean(widerstand_laufzeitmessung[116:136])

t[0] = np.mean(laufzeit[0:20])
t[1] = np.mean(laufzeit[20:37])
t[2] = np.mean(laufzeit[37:57])
t[3] = np.mean(laufzeit[57:77])
t[4] = np.mean(laufzeit[77:97])
t[5] = np.mean(laufzeit[97:116])
t[6] = np.mean(laufzeit[116:136])

sigma_R[0] = np.std(widerstand_laufzeitmessung[0:20], ddof=1) / np.sqrt(20)
sigma_R[1] = np.std(widerstand_laufzeitmessung[20:37], ddof=1) / np.sqrt(17)
sigma_R[2] = np.std(widerstand_laufzeitmessung[37:57], ddof=1) / np.sqrt(20)
sigma_R[3] = np.std(widerstand_laufzeitmessung[57:77], ddof=1) / np.sqrt(20)
sigma_R[4] = np.std(widerstand_laufzeitmessung[77:97], ddof=1) / np.sqrt(20)
sigma_R[5] = np.std(widerstand_laufzeitmessung[97:116], ddof=1) / np.sqrt(19)
sigma_R[6] = np.std(widerstand_laufzeitmessung[116:136], ddof=1) / np.sqrt(20)

sigma_t[0] = np.std(laufzeit[0:20], ddof=1) / np.sqrt(20)
sigma_t[1] = np.std(laufzeit[20:37], ddof=1) / np.sqrt(17)
sigma_t[2] = np.std(laufzeit[37:57], ddof=1) / np.sqrt(20)
sigma_t[3] = np.std(laufzeit[57:77], ddof=1) / np.sqrt(20)
sigma_t[4] = np.std(laufzeit[77:97], ddof=1) / np.sqrt(20)
sigma_t[5] = np.std(laufzeit[97:116], ddof=1) / np.sqrt(19)
sigma_t[6] = np.std(laufzeit[116:136], ddof=1) / np.sqrt(20)








"""
Kalibrieren des Potentiometers zur Längenmessung
"""

kalibrierung = p.lese_lab_datei("cassy\Kalibrierung.lab")

widerstand = kalibrierung[:,2]
strecke = kalibrierung[:,3]

# Plot Rohdaten
plt.figure(1)
plt.subplot(1, 1, 1)
plt.title("Messdaten zur Kalibration mit Fit")
plt.ylabel("Strecke / cm")
plt.xlabel("Widerstand / kOhm")
plt.errorbar(widerstand, strecke, yerr=0.03+0.07/np.sqrt(3), xerr=sigma_R, fmt="k.")



a, ea, b, eb, chi2, cov = p.lineare_regression_xy(widerstand, strecke, sigma_R, np.full(7, 0.03+0.07/np.sqrt(3)))

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
plt.figure(3)
plt.subplot(1,1,1)
#plt.errorbar(laufzeit, widerstand_laufzeitmessung, xerr=np.ones(laufzeit.size)*np.mean(sigma_t), yerr= np.ones(laufzeit.size)*np.mean(sigma_R), fmt="k.")
plt.errorbar(t, R, xerr=sigma_t, yerr= sigma_R, fmt="k.")
plt.title("Laufzeitmessung")
plt.xlabel("Laufzeit / s")
plt.ylabel("Widerstand / kOhm")

# Linreg Laufzeitmessung
#a, ea, b, eb, chi2, cov = p.lineare_regression_xy(laufzeit, widerstand_laufzeitmessung, sigma_t_array, sigma_R_array)
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(t, R, sigma_t*4.3, sigma_R*4.3)


# Plot Fit
x=np.arange(10)*0.001/9+0.00065
y=a*x+b
plt.plot(x, y)
dof = t.size -2
plt.figtext(0.15, 0.70, "$\Delta R / \Delta t = {:2.2f}(k\Omega /s)$\n$\sigma_a={:1.2f}k\Omega / t$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/dof))


# Schgallgeschwindigkeit berechnen
v_laufzeitmessung = cm_pro_kOhm * a/100
sigma_v_laufzeitmessung = v_laufzeitmessung * ((sigma_cm_pro_kOHm/cm_pro_kOhm) + (ea/a))
print("Laufzeitmessung ergibt:\n v={:4.4f}m/s \n sigma _v = {:2.4f}m/s".format(v_laufzeitmessung, sigma_v_laufzeitmessung))