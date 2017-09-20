# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:49:19 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum
from scipy.constants import sigma as sigma

#steigungen
p_schwarz, e_schwarz = 1.481856207e-9, 0.01 * p_schwarz
p_weis, e_weis = 1.4815e-9, 0.01 * p_weis
p_messing, e_messing = 1.433e-10, 0.01 * p_messing
p_spiegel, e_spiegel = 7.874e-11, 0.01 * p_spiegel


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




    
    