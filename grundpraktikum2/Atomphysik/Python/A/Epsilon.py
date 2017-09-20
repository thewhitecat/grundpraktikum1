# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:49:19 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
from scipy.constants import sigma as sigma
import Histogramme as h
import Regression as r

#steigungen
p_schwarz, ep_schwarz, b_schwarz, eb_schwarz = r.Auswertung(h.get_werte('schwarz'),plots = False)
p_weis, ep_weis, b_weis, eb_weis = r.Auswertung(h.get_werte('weiss'),plots = False)
p_messing, ep_messing, b_messing, eb_messing = r.Auswertung(h.get_werte('messing'),plots = False)
p_spiegel, ep_spiegel, b_spiegel, eb_spiegel = r.Auswertung(h.get_werte('spiegel'),plots = False)

p_list = np.array([p_schwarz,p_weis,p_messing,p_spiegel])
ep_list = np.array([ep_schwarz,ep_weis,ep_messing,ep_spiegel])
b_list = np.array([b_schwarz,b_weis,b_messing,b_spiegel])
eb_list = np.array([eb_schwarz,eb_weis,eb_messing,eb_spiegel])

#constants
kelvin = 273.15
k = 0.229
ek = k*0.0069
v = 10e-4
a, b = 1.0107638757247093, -3.3550993800564015
T0 = (23.7048701757+kelvin)*a+b


def get_epsilon_easy(p1,ep1):
    epsilon = p1*0.15**2*np.pi*v*k/(np.pi**2*(0.023/2)**2*(0.035/2)**2*sigma)
    epsilon_stat = epsilon * ep1/p1
    epsilon_syst = epsilon * ek/k
    return epsilon, epsilon_stat, epsilon_syst

print get_epsilon_easy(p_list,ep_list)

def get_epsilon_hard(p1,ep1,p0,ep0,string):
    data = h.get_werte(string)
    T, eT = a*(data[0]+kelvin)+b, data[1]*a+b
    
    eps = ((p0+p1*(T**4-T0**4))*v*0.15**2)/(np.pi*(0.035/2)**2*(0.023/2)**2*sigma*(T**4-T0**4))
    
    return eps

print get_epsilon_hard(p_schwarz, ep_schwarz, b_schwarz, eb_schwarz,'schwarz')
#,get_epsilon_hard('weiss'),get_epsilon_hard('messing'),get_epsilon_hard('spiegel')