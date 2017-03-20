# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:09:25 2017

@author: Sebastian
"""

import Praktikum as p
import matplotlib.pyplot as plt
import numpy as np


# Auswertung Eiswasser
data = p.lese_lab_datei("Lab\Temperatur_Eiswasser.lab")
temperatur = data[:,2] +273.15
druck = data[:,4]


# Rauschen -> Unsicherheit auf Einzelwerte
sigma_temp = np.std(temperatur, ddof=1)

minimum = 1000
for i in range(temperatur.size-1):
    neu = np.abs(temperatur[i]-temperatur[i+1])
    if (neu < minimum and neu > 0):
        minimum = neu
        
print(minimum)
# Plot Histogramm Rauschen im Eiswasser
plt.figure(2)
plt.hist(temperatur-273.15, bins = 30)


# Luftdruck im Raum mit Unsicherheit:
luftdruck = np.mean(druck)
# Unsicherheit ist durch Digitalisierung gegeben
sigma_luftdruck = 0.75 / np.sqrt(12)


# Kalibration Thermometer
data = p.lese_lab_datei("Lab\Temperatur_siedend.lab")
temperatur2 = data[-301:,2] + 273.15


# Schmelztemperatur von Wasser -> 273.15K erwartet
schmelz_temp = np.mean(temperatur)
# Unsicherheit des Mittelwertes
sigma_schmelz_temp = np.std(temperatur, ddof=1)/np.sqrt(temperatur.size)

# Siedetemperatur von Wasser -> 99.72C erwartet
siede_temp = np.mean(temperatur2)
#Unsicherheit des Mittelwertes
sigma_siede_temp = np.std(temperatur2, ddof=1)/np.sqrt(temperatur2.size)


# Kalibrierung durchführen, also Umrechnungsfaktor und Offset samt Unsicherheiten berechnen
m = 99.72/(siede_temp-schmelz_temp)
sigma_m = np.sqrt( sigma_siede_temp**2*(99.72/(siede_temp-schmelz_temp)**2)**2 + sigma_schmelz_temp**2*(99.72/(siede_temp-schmelz_temp)**2)**2)

b = 273.15 - (m*schmelz_temp)
sigma_b = np.sqrt( (sigma_m/m)**2 + (sigma_schmelz_temp/schmelz_temp)**2 )


# Plot Kalibrierung
plt.figure(1)
plt.errorbar([schmelz_temp, siede_temp], [273.15, 273.15+99.72], xerr=[sigma_schmelz_temp, sigma_siede_temp], fmt="o")
x = np.array([260, 385])
y = m*x+b
plt.plot(x, y)
plt.xlabel("$T_{gemessen} [K]$")
plt.ylabel("$T_{erwartet} [K]$")
plt.figtext(0.18, 0.75, "m = {:1.4f} $\pm$ {:1.4f}\nb = {:1.4f} $\pm$ {:1.4f}".format(m, sigma_m, b, sigma_b))