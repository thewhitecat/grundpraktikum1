# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:21:51 2017

@author: Sebastian
"""

import matplotlib.pyplot as plt
import numpy as np
import Praktikum as p
from scipy import odr
from scipy import constants as const

def new_fig():
    temp = plt.get_fignums()
    if temp:
        return max(temp)+1
    return 1


Gruppe = "C"
farbe = "spiegel"

# Temperaturkalibration
name = ""
if Gruppe != "A":
    name = "wasser"
fail = "kochend"
if Gruppe == "A":
    fail = "kochwn"

t_eis = np.mean(p.lese_lab_datei("{0:s}/eis{1:s}.lab".format(Gruppe, name))[:,3])
t_kochen = np.mean(p.lese_lab_datei("{0:s}/{1:s}{2:s}.lab".format(Gruppe, fail, name))[:,3])

# T_real = a* T_gemessen + b
kelvin = lambda x: np.array(x)+273.15

kalibration_a = 100.3/(t_kochen-t_eis)
kalibration_b = -kalibration_a*kelvin(t_eis)+kelvin(0)


temperatur = lambda x: kalibration_a*kelvin(x) + kalibration_b




# Raumtemperatur
raumtemp_messung = 0
t0 = p.lese_lab_datei("{0:s}/raumtemp/{1:d}.lab".format(Gruppe, raumtemp_messung))[:,3]
t0 = temperatur(np.mean(t0))





# Daten lesen

messbereich = 10

u = []
eu = []
t = []
et = []

for i in range(9):
    if i > 5:
        messbereich = 30
    try:
        data = p.lese_lab_datei("C/{0:s}/{1:d}.lab".format(farbe, 50+i*5))
    except IOError:
        continue
    u.append(np.mean(data[:,2]))
    t.append(temperatur(np.mean(data[:,3])))
    eu.append(np.std(data[:,2], ddof=1)/np.sqrt(125))
    et.append(np.std(data[:,3], ddof=1)/np.sqrt(125))
    
    minimal = []
    for j in range(len(data[:,2])-1):
        temp = abs(data[:,3][j]-data[:,3][j+1])
        if temp != 0:
            minimal.append(temp)
    
    minimal = min(minimal)

    #plt.figure(2*i)
    #plt.hist(data[:,2], bins = np.arange(min(data[:,2]), max(data[:,2])+2*messbereich/4096., 2*messbereich/4096.))
    #plt.title("{0:d} C - Spannung".format(50+5*i))
    
    #plt.figure(2*i+1)
    #plt.hist(data[:,3], bins = np.arange(min(data[:,3]), max(data[:,3])+minimal, minimal))
    #plt.title("{0:d} C - Temperatur".format(50+5*i))


t = np.array(t)
u = np.array(u)
et = np.array(et)
eu = np.array(eu)


# Linearer Fit

x = t**4 - t0**4
ex = 4*t**3*et

a, ea, b, eb, chi2, corr = p.lineare_regression_xy(x, u, ex, eu)
ndof = len(x)-2

plt.figure(new_fig(), [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(x, u, xerr = ex, yerr = eu, fmt = ".")
plt.plot(x, a*x+b)
plt.figtext(0.15, 0.65, "y = ax + b\na = ({0:1.3f} $\pm$ {1:1.3f})*1e-9 V/K$^4$ \nb = ({2:1.2f} $\pm$ {3:1.2f}) V \n$\chi^2$/ndof = {4:1.1f}".format(a*1e9, ea*1e9, b, eb, chi2/ndof))
plt.ylabel("Spannung [V]")
plt.xlabel("")
plt.xticks([])

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(x, u-a*x-b, yerr = np.sqrt(eu**2+(a*ex)**2), fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [V]")
plt.xlabel("$T^4 - T_0^4$ $[K^4]$")



# Epsilon berechnen

As = np.pi*(0.035/2)**2
Ae = np.pi*(0.023/2)**2
r = 0.108
empfindlichkeit = 0.276



p_ideal = lambda x: As*Ae*const.sigma*(x**4-t0**4)/np.pi/r**2
p_gemessen = lambda x: x*1e-4/empfindlichkeit
p_fit = lambda x: (a*x+b)*1e-4/empfindlichkeit
epsilon = p_gemessen(u)/p_ideal(t)

ee = epsilon * np.sqrt( (eu/u)**2 + (4*et/t)**2 )
ee_s = epsilon * 0.03

mittelwert, em = p.gewichtetes_mittel(epsilon, ee)
em = max(em, np.sqrt( (1./(len(epsilon)-1))*sum( (mittelwert-epsilon)**2/ee**2 )/sum(1/ee**2) ))
em_s = mittelwert*0.03


# Nicht-Linearer Fit

def f(B, x):
        return B[0]+ B[1]*x**B[2]

model  = odr.Model(f)
data   = odr.RealData(t, u, sx=et, sy=eu)
odr    = odr.ODR(data, model, beta0=[-1e-4*t0**4, const.sigma*np.mean(epsilon), 4.])
output = odr.run()
ndof = len(x)-2
chi2 = output.res_var*ndof

par = output.beta
sd = output.sd_beta


plt.figure(new_fig(), [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(t, u, xerr = et, yerr = eu, fmt = ".")
plt.plot(t, f(par, t))
plt.figtext(0.15, 0.6, "y = a + b x^c \na = ({0:1.3f} $\pm$ {1:1.3f}) V\nb = ({2:1.3f} $\pm$ {3:1.3f})*1e-9 V/K\nc = ({4:1.3f} $\pm$ {5:1.3f})\n$\chi^2/ndof$ = {6:1.1f}".format(par[0], sd[0], par[1]*1e9, sd[1]*1e9, par[2], sd[2], chi2/ndof))
plt.ylabel("Spannung [V]")
plt.xlabel("")
plt.xticks([])

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(t, u-f(par, t), yerr = np.sqrt(eu**2+(par[1]*par[2]*t**(par[2]-1)*et)**2), fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [V]")
plt.xlabel("Temperatur [K]")
