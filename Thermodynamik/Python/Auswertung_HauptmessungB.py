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
    
#Literaturwert für T in K
def Lambda(T):
    T = T-273.15
    x_C_2 = [60, 80, 100]
    y_2 = [42.482, 41.585, 40.657]

    a_2 = [60, 100]
    b_2 = [42.482, 40.657]

    m = (y_2[2] - y_2[0])/(x_C_2[2] - x_C_2[0])
    b = y_2[0] - m * x_C_2[0]
    return np.round((m * T + b), 3)

data = p.lese_lab_datei("Lab\Hauptmessung.lab")

laufzeit = data[50:,1]
druck = data[50:,4]
temperatur = data[50:,2]

R = 8.314
                 
# Rauschwerte -> Fehler auf Einzelwerte
sigma_p = np.sqrt((0.75/np.sqrt(12))**2+0.37**2) # mit Digitlisierungsfehler
sigma_t = 0.1


# Druck und Temperatur beim Sieden
p0 = 1000
temp0 = 373.15

# Korrekturwerte für Druck und Temperatur
m = 1.013
sigma_m = 0.002
b = -0.53
sigma_b = 0.0002
#sigma_sys_t = np.srt( (m*temperatur)**2 *(sigma_m/m)**2 + sigma_b**2)
offset_druck = 0





# Plot Rohdaten vs Zeit
plt.figure(1)
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
plt.xlabel("Temperatur [K]")
plt.ylabel("Druck [hPa]")


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
n = 6
n = n+2
intervall = kehrwert_temp.size/n
unterteilung = np.arange(1,n-1) * intervall



sigma_steigung_array = np.empty(n-2)
steigung_array = np.empty(n-2)

for i in range(unterteilung.size):
    # Plot Daten
    x, y, ex, ey, a, ea, b, eb, chi2, cov = gerade_an_intervall(kehrwert_temp, log_druck, sigma_t_kehr, sigma_p_log, unterteilung[i], intervall/2)
    steigung_array[i] = a
    sigma_steigung_array[i] = ea
    if (i == 1):
        plt.figure(4)
        plt.errorbar(x, y, xerr=ex, yerr=ey, fmt=".")
        plt.xlabel( "$(1/T - 1/T_0) [1/s]$")
        plt.ylabel( "$ln(p/p_0) [hPa]$")
        plt.xticks(rotation=0)
        x2 = np.array([x[-1], x[0]])
        y2 = a*x2+b
        plt.plot(x2, y2, color="k")
        dof = intervall-1
        plt.figtext(0.7, 0.6, "a = {:2.3f}K\n$\sigma_a$ = {:2.3f}K\nb= {:2.3f}\n$\sigma_b$={:2.3f}\n$chi^2$/dof = {:2.3f}".format(a, ea, b, eb, chi2/dof))
    
        plt.figure(3)
        plt.axvline(x[0])
        plt.axvline(x[-1])
        # Plot Residuen
        plt.figure(5)
        plt.subplot(2, 1, 1)
        plt.errorbar(x, y-(a*x+b), yerr=np.sqrt(ey**2 + a**2*ex**2), fmt="k.")
        plt.xlabel("$(1/T - 1/T_0) [1/s]$")
        plt.ylabel("Residuen [hPa]")
        plt.axhline(0, linestyle="dashed")
        plt.xticks(rotation=0)
    temp = 1/(kehrwert_temp[unterteilung[i]]+(1/temp0))
    print ("\nTemperatur = {:3.3f}\n$\Lambda$ = {:3.3f}, $\sigma_\Lambda$ = {:3.3f}\n".format(temp, -a*R/1000, ea*R/1000))



plt.figure(4+2*(n-2)+2)
# Verdampfungsenthalpie in kJ/mol
enthalpie = -steigung_array * R /1000
sigma_enthalpie = sigma_steigung_array * R /1000
plt.errorbar(1/(kehrwert_temp[intervall:(n-1)*intervall:intervall]+(1/temp0)), enthalpie, xerr=sigma_t, yerr=sigma_enthalpie, fmt=".")
plt.xlabel("Temperatur [K]")
plt.ylabel("Verdampfungsenthalpie [kJ/mol]")

# Literaturwerte
x = [60+273.15, 100+273.15]
y = [42.482, 40.657]
plt.xlim(60+273.15, 100+273.15)
plt.plot(x, y)


# Abweichung von Literaturwerten
abweichung = (enthalpie - Lambda(1/(kehrwert_temp[intervall:(n-1)*intervall:intervall]+(1/temp0))) )/sigma_enthalpie


#plt.figure(4+2*n+2)
#plt.plot(laufzeit, kehrwert_temp, linestyle="dotted")
#plt.ylabel("(1/T -1/T_0) [1/K]")
#plt.xlabel("Laufzeit [s]")