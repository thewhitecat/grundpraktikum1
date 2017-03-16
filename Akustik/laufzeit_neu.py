# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:26:46 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

# Daten einlesen
laufzeitmessung = p.lese_lab_datei("cassy\Laufzeit.lab")
laufzeit = laufzeitmessung[:,2]
widerstand_laufzeitmessung = laufzeitmessung[:,3]

# Einzelne Messreihen trennen
messreihe_widerstand = np.array([ widerstand_laufzeitmessung[0:20], widerstand_laufzeitmessung[20:37],   widerstand_laufzeitmessung[37:57]   , widerstand_laufzeitmessung[57:77], widerstand_laufzeitmessung[77:97], widerstand_laufzeitmessung[97:116], widerstand_laufzeitmessung[116:136] ])
messreihe_laufzeit = np.array([ laufzeit[0:20], laufzeit[20:37],      laufzeit[37:57] , laufzeit[57:77], laufzeit[77:97], laufzeit[97:116], laufzeit[116:136] ])

# Stat. Digitalisierungsfehler Widerstand (auf Zeit vernachlässigbar):
sigma_dig = 10/(4096*np.sqrt(12))

# Mittelwerte und Unsicherheiten auf Mittelwerte berechnen
R = np.empty(7)
t= np.empty(7)
sigma_R = np.empty(7)
sigma_t = np.empty(7)
for i in range(0,7):
    R[i] = np.mean(messreihe_widerstand[i])
    t[i] = np.mean(messreihe_laufzeit[i])
    # Fehler auf Mittelwerte
    sigma_R[i] = np.std(messreihe_widerstand[i], ddof=1)/np.sqrt(messreihe_widerstand[i].size)
    # Stat. Digitalisierungsfehler addieren
    sigma_R[i] = np.sqrt(sigma_R[i]**2+sigma_dig**2)
    sigma_t[i] = np.std(messreihe_laufzeit[i], ddof=1)/np.sqrt(messreihe_widerstand[i].size)


# Wert aus Kalibration (systematischer Fehler):
k = 15.99
ek = 0.07



# Plot Mittelwerte
plt.figure(1)
plt.errorbar(t, R, xerr=sigma_t, yerr= sigma_R, fmt="k.")
plt.title("Laufzeitmessung")
plt.xlabel("Laufzeit / s")
plt.ylabel("Widerstand / $k\Omega$")


# Lineare Regression
a, ea, b, eb, chi2, cov = p.lineare_regression_xy(t, R, sigma_t, sigma_R)



# Plot fit
x = t
y = a*x +b
plt.plot(x, y)
dof = t.size -2
plt.figtext(0.15, 0.60, "$a = {:2.2f}(k\Omega /s)$   \n$sigma_a={:1.2f}k\Omega / s$   \n$b={:2.2f}k\Omega$   \n$\sigma_b={:2.2f}k\Omega$   \n$\chi ^2 /dof ={:2.3f}$".format(a, ea, b, eb, chi2/dof))


# Residuen
sigma_residuen = np.empty(7)
for i in range(7):
    sigma_residuen[i] = np.sqrt(sigma_R[i]**2+a**2*sigma_t[i]**2)

y=R-y
plt.figure(2)
plt.subplot(2,1,1)
plt.errorbar(x, y, yerr=sigma_residuen, fmt="k.", linestyle="")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen / $k\Omega$")
plt.xlabel("t / s")
plt.title("Residuenverteilung")



# Schallgeschwindigkeit und Fehler berechnen
v = a * k /100    # cm/s in m/s umrechnen
#Statistischer Fehler nur aus a
sigma_stat = v * (ea/a)
# Systematischer Fehler: nur aus k
sigma_sys = v* (ek/k)
# Quadratisch addieren:
sigma_v = np.sqrt(sigma_stat**2 + sigma_sys**2)

print sigma_R
print "\n"
print sigma_t*1000
print "\n"
print ("v = ({0:3.3f}+-{1:1.3f}+-{2:1.3f})m/s = ({0:3.3f}+-{3:1.3f})m/s".format(v, sigma_stat, sigma_sys, sigma_v))
print ("Abweichung von Theorie: {:f}".format((v-345.14)/sigma_v))


