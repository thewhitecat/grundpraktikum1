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
Kalibrieren des Potentiometers zur Längenmessung
"""

kalibrierung = p.lese_lab_datei("cassy\Kalibrierung.lab")

widerstand = kalibrierung[:,2]
strecke = kalibrierung[:,3]

# Plot Rohdaten
plt.figure(1)
plt.subplot(1, 1, 1)
plt.title("Messdaten zur Kalibration")
plt.ylabel("Strecke / cm")
plt.xlabel("Widerstand / kOhm")
plt.errorbar(widerstand, strecke, yerr=0.5, xerr=0.01*widerstand+0.01, fmt="k.")



a, ea, b, eb, chi2, cov = p.lineare_regression_xy(widerstand, strecke, 0.001*widerstand, np.full(7, 0.5))

cm_pro_kOhm = np.abs(a)
sigma_cm_pro_kOHm = ea

# Plot Fit
x=np.arange(10)*2.5/10 +0.3
y=a*x+b
plt.plot(x, y)
plt.figtext(0.55, 0.71, "$\Delta s = {:2.2f}(cm/k\Omega)*\Delta R$\n$\sigma_a={:1.2f}cm / k\Omega$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/2))






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
R[1] = np.mean(widerstand_laufzeitmessung[21:38])
R[2] = np.mean(widerstand_laufzeitmessung[39:59])
R[3] = np.mean(widerstand_laufzeitmessung[60:80])
R[4] = np.mean(widerstand_laufzeitmessung[81:101])
R[5] = np.mean(widerstand_laufzeitmessung[102:121])
R[6] = np.mean(widerstand_laufzeitmessung[122:142])

t[0] = np.mean(laufzeit[0:20])
t[1] = np.mean(laufzeit[21:38])
t[2] = np.mean(laufzeit[39:59])
t[3] = np.mean(laufzeit[60:80])
t[4] = np.mean(laufzeit[81:101])
t[5] = np.mean(laufzeit[102:121])
t[6] = np.mean(laufzeit[122:142])

sigma_R[0] = np.std(widerstand_laufzeitmessung[0:20])
sigma_R[1] = np.std(widerstand_laufzeitmessung[21:38])
sigma_R[2] = np.std(widerstand_laufzeitmessung[39:59])
sigma_R[3] = np.std(widerstand_laufzeitmessung[60:80])
sigma_R[4] = np.std(widerstand_laufzeitmessung[81:101])
sigma_R[5] = np.std(widerstand_laufzeitmessung[102:121])
sigma_R[6] = np.std(widerstand_laufzeitmessung[122:142])

sigma_t[0] = np.std(laufzeit[0:20])
sigma_t[1] = np.std(laufzeit[21:38])
sigma_t[2] = np.std(laufzeit[39:59])
sigma_t[3] = np.std(laufzeit[60:80])
sigma_t[4] = np.std(laufzeit[81:101])
sigma_t[5] = np.std(laufzeit[102:121])
sigma_t[6] = np.std(laufzeit[122:142])

"""
plt.figure(2,[6, 21])

plt.subplot(7, 1, 1)
plt.hist(r1, bins=20)
plt.figtext(0.91, 0.85, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r1), np.std(r1)))

plt.subplot(7, 1, 2)
plt.hist(r2, bins=20)
plt.figtext(0.91, 0.74, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r2), np.std(r2)))

plt.subplot(7, 1, 3)
plt.hist(r3, bins=20)
plt.figtext(0.91, 0.63, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r3), np.std(r3)))

plt.subplot(7, 1, 4)
plt.hist(r4, bins=20)
plt.figtext(0.91, 0.50, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r4), np.std(r4)))

plt.subplot(7, 1, 5)
plt.hist(r5, bins=20)
plt.figtext(0.91, 0.39, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r5), np.std(r5)))

plt.subplot(7, 1, 6)
plt.hist(r6, bins=20)
plt.figtext(0.91, 0.27, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r6), np.std(r6)))

plt.subplot(7, 1, 7)
plt.hist(r7, bins=20)
plt.figtext(0.91, 0.16, "$\mu = {:1.4f}$\n$\sigma={:1.4f}$".format(np.mean(r7), np.std(r7)))
"""



plt.figure(3)
plt.subplot(1,1,1)
plt.errorbar(t, R, xerr=sigma_t, yerr= sigma_R, fmt="k.")
plt.title("Laufzeitmessung")
plt.xlabel("Laufzeit / s")
plt.ylabel("Widerstand / kOhm")


a, ea, b, eb, chi2, cov = p.lineare_regression_xy(t, R, sigma_t, sigma_R)


# Plot Fit
x=np.arange(10)*0.0008/10+0.0008
y=a*x+b
plt.plot(x, y)
plt.figtext(0.15, 0.70, "$\Delta R / \Delta t = {:2.2f}(k\Omega /s)$\n$\sigma_a={:1.2f}k\Omega / t$\n$\chi ^2 /dof ={:2.3f}$".format(a, ea, chi2/2))


"""
Schallgeschwindigkeit berechnen
"""
v_laufzeitmessung = cm_pro_kOhm * a/100
sigma_v_laufzeitmessung = v_laufzeitmessung * np.sqrt( (sigma_cm_pro_kOHm/cm_pro_kOhm)**2 + (ea/a)**2 )/100
print("Laufzeitmessung ergibt:\n v={:4.4f}m/s \n sigma _v = {:2.4f}m/s".format(v_laufzeitmessung, sigma_v_laufzeitmessung))
