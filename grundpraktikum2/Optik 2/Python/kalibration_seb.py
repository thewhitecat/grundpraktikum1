# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 14:16:37 2017

@author: Sebastian
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

# Wellenlänge Laser
laser = 632.8e-9
sig_laser = 0.1e-9

m, s = np.genfromtxt("..\Kalibration_B.txt", skip_header=1, delimiter=",", unpack=True)
s*=1e-3
sig_s = 0.01e-3/np.sqrt(12)

# 2d = m lambda
# d = ks
# 2 s/lambda = m /k

y = 2*s/laser
sig_y = 2 * np.sqrt( (sig_s/laser)**2 + (s*sig_laser/laser**2)**2 )

a, ea, b, eb, chi2, corr = p.lineare_regression(m, y, np.full(len(m),sig_y))
k = 1/a
ek = ea/a**2


plt.figure(1, [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(m, y, yerr=sig_y, fmt=".")
plt.plot(m, a*m+b)
plt.figtext(0.2, 0.65, "y = m/k\n$k = ({0:3.4f} \pm {1:3.4f})$\nb = $({2:3.2f} \pm {3:3.2f})$\n$\chi^2/ndof$ = {4:3.2f}".format(k, ek, b, eb, chi2/(len(m)-2)))
plt.ylabel("2s/$\lambda$")
plt.xlabel("m")

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(m, y - a*m -b, yerr=sig_y, fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("m")


############################
# 
#   Bestimmung Wellenlänge
#
############################

m, s, s2 = np.genfromtxt("..\Wellenlaenge_B.txt", skip_header=1, delimiter=",", unpack=True)
s*=1e-3
#s = s[0:-1]
m = m[0:len(s)]
# 2 ks = lambda m

y = 2*k*s
ey = y* np.sqrt( (ek/k)**2 + (sig_s/s)**2 )


a, ea, b, eb, chi2, corr = p.lineare_regression(m, y, ey)

plt.figure(2, [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(m, y, yerr=ey, fmt=".")
plt.plot(m, a*m+b)
plt.figtext(0.2, 0.65, "2 k s = $\lambda$ m\n$\lambda = ({0:3.2f} \pm {1:3.2f})nm$\nb = $({2:3.2f} \pm {3:3.2f})$\n$\chi^2/ndof$ = {4:3.2f}".format(a*1e9, ea*1e9, b, eb, chi2/(len(m)-2)))
plt.ylabel("2 k s")
plt.xlabel("m")

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(m, y - a*m -b, yerr=ey, fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen")
plt.xlabel("m")


