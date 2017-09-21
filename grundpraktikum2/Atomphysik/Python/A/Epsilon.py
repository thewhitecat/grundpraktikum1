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

eps_rel_easy = p_list/p_schwarz
eps_rel_easy_stat = eps_rel_easy * (ep_list)/(p_list)
eps_rel_easy_syst = eps_rel_easy * (ep_schwarz)/(p_schwarz)
#constants
kelvin = 273.15
k = 0.229
ek = 0.0069
v = 1e-4
a, b = 1.0107638757247093, -3.3550993800564015
T0 = (23.7048701757+kelvin)*a+b

# durch konstante teilen -> werte sind seltsam + mist
#mit konstante mal nehmen (entgegen skript etc)-> werte gut
#?!?!?!?!??!?!?!?!?!?!?

def get_epsilon_easy(p1,ep1):
    epsilon = p1*0.108**2*np.pi*v/(k*np.pi**2*(0.023/2)**2*(0.035/2)**2*sigma)
    epsilon_stat = epsilon * ep1/p1
    epsilon_syst = epsilon * ek/k
    return epsilon, epsilon_stat, epsilon_syst

print get_epsilon_easy(p_list,ep_list)

def get_epsilon_hard(p1,ep1,p0,ep0,string):
    data = h.get_werte(string)
    T, eT = a*(data[0]+kelvin)+b, data[1]*a+b
    eps = ((p0+p1*(T**4-T0**4))*v*(0.108**2))/(k*np.pi*(0.035/2)**2*(0.023/2)**2*sigma*(T**4-T0**4))
    return eps

def get_epsilon(string):
    data = h.get_werte(string)
    T, eT = a*(data[0]+kelvin)+b, data[1]*a+b
    U, eU = data[2], data[3]
    
    eps = (U*v*0.108**2*np.pi)/((k*np.pi**2*(0.035/2)**2*(0.023/2)**2*sigma*(T**4-T0**4)))
    eps_stat = np.sqrt((eU/U)**2*eps + (eps*eT*4*T**3/(T**4))**2)
    eps_syst = np.sqrt((ek/k)**2*eps**2)
    return eps,eps_stat,eps_syst
    
def get_epsilon_rel():        
    schwarz = get_epsilon('schwarz')
    weiss =  get_epsilon('weiss')
    messing = get_epsilon('messing')
    spiegel = get_epsilon('spiegel')
    

    
    
schwarz = get_epsilon('schwarz')
weiss =  get_epsilon('weiss')
messing = get_epsilon('messing')
spiegel = get_epsilon('spiegel')
