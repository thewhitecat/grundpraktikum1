# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:09:25 2017

@author: Sebastian
"""

import Praktikum as p
import matplotlib.pyplot as plt
import numpy as np


# Auswertung Rauschen
data = p.lese_lab_datei("CASSY\Rauschmessungen.lab")
temperatur = data[:,3] +273.15
druck = data[:,2]


# Rauschen -> Unsicherheit auf Einzelwerte
sigma_temp = np.std(temperatur, ddof=1)


# Luftdruck im Raum mit Unsicherheit:
luftdruck = np.mean(druck)
# Unsicherheit ist durch Digitalisierung gegeben
sigma_luftdruck = 0.75 / np.sqrt(12)


# Kalibration Thermometer
data = p.lese_lab_datei("CASSY\Temperatur_siedend.lab")
temperatur2 = data[-301:,3] + 273.15


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