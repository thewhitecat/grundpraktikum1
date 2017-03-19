# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:42:15 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt


def untermenge_daten(x,a,b,c,d,e,f,x0,x1):
    '''
    Extrahiere kleinere Datensaetze aus (x,y), so dass x0 <= x <= x1
    '''
    xn=[]
    an=[]
    bn=[]
    cn=[]
    dn=[]
    en=[]
    fn=[]
    for i,v in enumerate(x):
        if x0<=v<=x1:
            xn.append(x[i])
            an.append(a[i])
            bn.append(b[i])
            cn.append(c[i])
            dn.append(d[i])
            en.append(e[i])
            fn.append(f[i])

    return (np.array(xn),np.array(an), np.array(bn), np.array(cn), np.array(dn),
            np.array(en), np.array(fn))

    
#Literaturwert für T in K
def literaturwert(T):
    T = T-273.15
    x_C_2 = [60, 80, 100]
    y_2 = [42.482, 41.585, 40.657]

    #a_2 = [60, 100]
    #b_2 = [42.482, 40.657]

    m = (y_2[2] - y_2[0])/(x_C_2[2] - x_C_2[0])
    b = y_2[0] - m * x_C_2[0]
    return np.round((m * T + b), 3)

data = p.lese_lab_datei("CASSY\Hauptmessung.lab")

laufzeit = data[:-140,1]
druck = data[:-140,2]
temperatur = data[:-140,3] + 273.15
                 
                 
R = 8.314

# Korrekturwerte für Druck und Temperatur
m = 1.0252
sigma_m = 0.0001
b = -9.06
sigma_b = 0.0003
offset_druck = 11.25   
              
# Rauschwerte -> Fehler auf Einzelwerte
sigma_p_stat = 0.75/np.sqrt(12)
sigma_p_sys = 0.75/np.sqrt(12)
sigma_t_stat = 0.12
sigma_t_sys = np.sqrt(temperatur**2*sigma_m**2 + m**2*sigma_t_stat**2 + sigma_b**2)

# Druck und Temperatur beim Sieden
p0 = 1005.0
temp0 = 372.87







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
plt.errorbar(temperatur, druck, linestyle="dotted")
plt.title("Dampfdruckkurve")
plt.xlabel("Temperatur [K]")
plt.ylabel("Druck [hPa]")


# Temperatur korrigieren
temperatur = m * temperatur + b
druck = druck + offset_druck

# Druck und Temperatur für lin Reg transformieren
log_druck = np.log(druck/p0)
kehrwert_temp = (1/temperatur-1/temp0)
sigma_p_log_stat = sigma_p_stat/druck
sigma_t_kehr_stat = sigma_t_stat/(temperatur**2)
sigma_p_log_sys = sigma_p_sys/druck
sigma_t_kehr_sys = sigma_t_sys/(temperatur**2)



# Plot Daten
plt.figure(3)
plt.errorbar(kehrwert_temp, log_druck, xerr=sigma_t_kehr_stat, yerr=sigma_p_log_stat, fmt="k.")
plt.xlabel("$(1/T - 1/T_0)$ [1/K]")
plt.ylabel("ln($p/p_0$)")

a, ea, b, eb, chi2, cov = p.lineare_regression_xy(kehrwert_temp, log_druck, sigma_t_kehr_stat, sigma_p_log_stat)

# Plot fit
x = np.array([kehrwert_temp[-1], kehrwert_temp[0]])
y = a*x+b
plt.plot(x, y)
dof = kehrwert_temp.size -2
plt.figtext(0.65, 0.6, "a = {:2.3f}K\n$\sigma_a$ = {:2.3f}K\nb= {:2.3f}\n$\sigma_b$={:2.3f}\n$chi^2$/dof = {:2.3f}".format(a, ea, b, eb, chi2/dof))

# Residuen
plt.figure(4)
y = log_druck - a*kehrwert_temp - b
plt.errorbar(kehrwert_temp, y, yerr=np.sqrt(sigma_p_log_stat**2 + a**2*sigma_t_kehr_stat**2), fmt=".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("(1/T - 1/$T_0$) [1/K]")





# Stückweiser fit, jeweils über 1/n * Temperaturbereich
n = 6
temperaturbereich = temperatur[0] - temperatur[-1]
intervallgrenzen = temperatur[-1] + np.arange(n+1)*temperaturbereich/n


sigma_stat_steigung_array = np.empty(n)
sigma_sys_steigung_array = np.empty(n)
steigung_array = np.empty(n)
temp_array = np.empty(n)
enthalpie = np.empty(n)
sigma_sys_enthalpie_array = np.empty(n)

for i in range(n):
    # Temperaturbereich auswählen
    tmin = intervallgrenzen[i]
    tmax = intervallgrenzen[i+1]
    
    # Untermengen selektieren und fit durchführen
    egal, x, y, ex_stat, ey_stat, ex_sys, ey_sys = \
    untermenge_daten(temperatur, kehrwert_temp, log_druck, sigma_t_kehr_stat,
                     sigma_p_log_stat, sigma_t_kehr_sys, sigma_p_log_sys, tmin, tmax)
    # Eigentlicher Fit
    a, ea, b, eb, chi2, cov = p.lineare_regression_xy(x, y, ex_stat, ey_stat)
    
    # Verschiebungen um syst. Unsicherheiten
    # Verschiebung in 1/T
    a_t1, ea_p1, b_t1, eb_t1, chi2_t1, cov_t1 = p.lineare_regression_xy(x-ex_sys, y, ex_stat, ey_stat)
    a_t2, ea_t2, b_t2, eb_t2, chi2_t2, cov_t2 = p.lineare_regression_xy(x+ex_sys, y, ex_stat, ey_stat)
    # Verschiebung in ln(p)
    a_p1, ea_p1, b_p1, eb_p1, chi2_p1, cov_p1 = p.lineare_regression_xy(x, y-ey_sys, ex_stat, ey_stat)
    a_p2, ea_p2, b_p2, eb_p2, chi2_p2, cov_p2 = p.lineare_regression_xy(x, y+ey_sys, ex_stat, ey_stat)
    
    # Eigentliche Steigung für aktuellen Bereich speichern
    steigung_array[i] = a
    sigma_stat_steigung_array[i] = ea
                             
    # Systematische Unsicherheit auf Steigung berechnen
    sigma_sys_steigung_array[i] = np.sqrt( (np.abs(a_t2-a)+np.abs(a_t1-a))**2/4 + (np.abs(a_p2-a)+ np.abs(a_p1-a))**2/4 )
    enthalpie[i] = -a *R /1000
    enthalpie_1 = - a_t1*R/1000
    enthalpie_2 = - a_t2*R/1000
    enthalpie_3 = - a_p1*R/1000
    enthalpie_4 = - a_p2*R/1000
    sigma_sys_enthalpie_array[i] = np.sqrt( (np.abs(enthalpie_2-enthalpie[i])+np.abs(enthalpie_1-enthalpie[i]))**2/4 + (np.abs(enthalpie_3-enthalpie[i])+ np.abs(enthalpie_4-enthalpie[i]))**2/4 )
    
    if (i == 4):
        plt.figure(5)
        plt.errorbar(x, y, xerr=ex_stat, yerr=ey_stat, fmt=".")
        plt.xlabel( "$(1/T - 1/T_0) [1/K]$")
        plt.ylabel( "$ln(p/p_0)$")
        plt.xticks(rotation=0)
        x2 = np.array([x[-1], x[0]])
        y2 = a*x2+b
        plt.plot(x2, y2, color="k")
        dof = x.size-2
        plt.figtext(0.7, 0.6,
        "a = {:2.3f}K\n$\sigma_a$ = {:2.3f}K\nb= {:2.3f}\n$\sigma_b$={:2.3f}\n$chi^2$/dof = {:2.3f}"\
             .format(a, ea, b, eb, chi2/dof))
    
        plt.figure(3)
        plt.axvline(x[0])
        plt.axvline(x[-1])
        # Plot Residuen
        plt.figure(6)
        plt.subplot(2, 1, 1)
        plt.errorbar(x, y-(a*x+b), yerr=np.sqrt(ey_stat**2 + a**2*ex_stat**2), fmt="k.")
        plt.xlabel("$(1/T - 1/T_0) [1/K]$")
        plt.ylabel("Residuen")
        plt.axhline(0, linestyle="dashed")
        plt.xticks(rotation=0)
    mittlere_temp = (tmin+tmax)/2
    temp_array[i] = mittlere_temp
    print ("\nTemperatur = {:3.3f} ({:3.3f} bis {:3.3f})\n$\Lambda$ = {:3.3f}, $\sigma_\Lamda$ = {:3.3f}\n"\
           .format(mittlere_temp, tmin, tmax, -a*R/1000, ea*R/1000))








plt.figure(7)
# Verdampfungsenthalpie in kJ/mol
#enthalpie = -steigung_array * R /1000
sigma_enthalpie_stat = sigma_stat_steigung_array * R /1000
sigma_enthalpie_sys = sigma_sys_steigung_array * R/1000
sigma_enthalpie = np.sqrt(sigma_enthalpie_stat**2 + sigma_enthalpie_sys**2)
plt.errorbar(temp_array, enthalpie, xerr=sigma_t_stat, yerr=sigma_enthalpie, fmt=".")
plt.xlabel("Temperatur [K]")
plt.ylabel("Verdampfungsenthalpie [kJ/mol]")

# Literaturwerte
x = np.array([temp_array[0]-5, temp_array[-1]+5])
y = literaturwert(x)
plt.xlim(temp_array[0]-5, temp_array[-1]+5)
plt.plot(x, y)


# Abweichung von Literaturwerten
abweichung = (enthalpie - literaturwert(temp_array) )/sigma_enthalpie



#plt.figure(4+2*n+2)
#plt.plot(laufzeit, kehrwert_temp, linestyle="dotted")
#plt.ylabel("(1/T -1/T_0) [1/K]")
#plt.xlabel("Laufzeit [s]")