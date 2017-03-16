# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:42:15 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt


def gerade_an_intervall(x, y, ex, ey, wert = 0, intervall = 0):
    x = x[wert-intervall:wert+intervall+1]
    y = y[wert-intervall:wert+intervall+1]
    ex= ex[wert-intervall:wert+intervall+1]
    ey= ey[wert-intervall:wert+intervall+1]
    a, ea, b, eb, chi2, cov = p.lineare_regression_xy(x, y, ex, ey)
    return x, y, ex, ey, a, ea, b, eb, chi2, cov
    


data = p.lese_lab_datei("Lab\Hauptmessung.lab")

laufzeit = data[50:,1]
druck = data[50:,4]
temperatur = data[50:,2]

R = 8.314
                 
# Rauschwerte -> Fehler auf Einzelwerte
sigma_p = 0.37
sigma_t = 0.035


# Druck und Temperatur beim Sieden
p0 = 1000
temp0 = 373.15

# Korrekturwerte für Druck und Temperatur
m = 1.013
sigma_m = 0.002
b = -0.53
sigma_b = 0.0002
#sigma_sys_t = np.srt( (m*temperatur)**2 *(sigma_m/m)**2 + sigma_b**2)
offset_druck = -16





# Plot Rohdaten vs Zeit
plt.figure(1)
plt.title("Rohdaten")
plt.subplot(2, 1, 1)
plt.plot(laufzeit, druck, linestyle="dotted")
plt.xlabel("Laufzeit / s")
plt.ylabel("Absolutdruck / hPa")

plt.subplot(2, 1, 2)
plt.plot(laufzeit, temperatur, linestyle="dotted")
plt.xlabel("Laufzeit / s")
plt.ylabel("Temperatur / K")

# Dampdruckkruve
plt.figure(2)
plt.plot(temperatur, druck, linestyle="dotted")
plt.title("Dampfdruckkurve")


# Temperatur korrigieren
temperatur = m * temperatur + b
druck = druck + offset_druck

# Druck und Temperatur für lin Reg transformieren
log_druck = np.log(druck/p0)
kehrwert_temp = (1/temperatur-1/temp0)
sigma_p_log = sigma_p/druck
sigma_t_kehr = sigma_t/(temperatur**2)



# Plot Daten
plt.figure(3)
plt.errorbar(kehrwert_temp, log_druck, xerr=sigma_t_kehr, yerr=sigma_p_log, fmt="k.")
plt.xlabel("$(1/T - 1/T_0)$ [1/K]")
plt.ylabel("ln($p/p_0$)")

#a, ea, b, eb, chi2, cov = p.lineare_regression_xy(kehrwert_temp, log_druck, sigma_t_kehr, sigma_p_log)

# Plot fit
#x = np.array([kehrwert_temp[-1], kehrwert_temp[0]])
#y = a*x+b
#plt.plot(x, y)
#dof = kehrwert_temp.size -2
#plt.figtext(0.65, 0.6, "a = {:2.3f}K\n$\sigma_a$ = {:2.3f}K\nb= {:2.3f}\n$\sigma_b$={:2.3f}\n$chi^2$/dof = {:2.3f}".format(a, ea, b, eb, chi2/dof))







# Stückweiser fit, jeweils
n = 15
n = n+2
intervall = kehrwert_temp.size/n
unterteilung = np.arange(n-1)[1:] * intervall



sigma_steigung_array = np.empty(n-2)
steigung_array = np.empty(n-2)

for i in range(unterteilung.size):
    # Plot Daten
    plt.figure(5+2*i)
    x, y, ex, ey, a, ea, b, eb, chi2, cov = gerade_an_intervall(kehrwert_temp, log_druck, sigma_t_kehr, sigma_p_log, unterteilung[i], intervall/2)
    steigung_array[i] = a
    sigma_steigung_array[i] = ea
    plt.errorbar(x, y, xerr=ex, yerr=ey, fmt=".")
    x2 = np.array([x[-1], x[0]])
    y2 = a*x2+b
    plt.plot(x2, y2, color="k")
    dof = intervall-1
    plt.figtext(0.7, 0.6, "a = {:2.3f}K\n$\sigma_a$ = {:2.3f}K\nb= {:2.3f}\n$\sigma_b$={:2.3f}\n$chi^2$/dof = {:2.3f}".format(a, ea, b, eb, chi2/dof))
    
    # Plot Residuen ohne Fehler
    plt.figure(5+2*i+1)
    plt.subplot(2, 1, 1)
    plt.errorbar(x, y-(a*x+b), yerr=np.sqrt(ey**2 + a**2*ex**2), fmt="k.")
    plt.axhline(0, linestyle="dashed")
    temp = 1/(kehrwert_temp[unterteilung[i]]+(1/temp0))
    print ("\nTemperatur = {:3.3f}\n$\Lambda$ = {:3.3f}, $\sigma_\Lambda$ = {:3.3f}\n".format(temp, -a*R/1000, ea*R/1000))


plt.figure(4+2*(n-2)+2)
# Verdampfungsenthalpie in kJ/mol
enthalpie = -steigung_array * R /1000
sigma_enthalpie = sigma_steigung_array * R /1000
plt.errorbar(1/(kehrwert_temp[intervall:(n-1)*intervall:intervall]+(1/temp0)), enthalpie, xerr=sigma_t, yerr=sigma_enthalpie, fmt=".")


#plt.figure(4+2*n+2)
#plt.plot(laufzeit, kehrwert_temp, linestyle="dotted")
#plt.ylabel("(1/T -1/T_0) [1/K]")
#plt.xlabel("Laufzeit [s]")