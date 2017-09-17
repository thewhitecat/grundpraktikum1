# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:21:35 2017

@author: Sebastian
"""

import Praktikum as p
import numpy as np
import matplotlib.pyplot as plt

ef = 5

widerstand = "10"
data = p.lese_lab_datei("{0:s}Ohm.lab".format(widerstand))

U = data[:,2]
I = data[:,3]

phi = data[:,4]

UL = data[:,5]

UC = data[:,6]

f = data[:,8]



### Breite Strom

def strombreite(f, I):
    i = np.argmax(I)
    f0 = f[i]
    Imax = np.max(I)
    
    f1 = f[np.argmax(-np.abs(I[0:i]-Imax/np.sqrt(2)))]
    
    f2 = f[np.argmax(-np.abs(I[i:-1]-Imax/np.sqrt(2)))+i]
    
    return Imax, f0, f1, f2

Imax, f0, f1, f2 = strombreite(f, I)

plt.figure(1)
plt.plot(f, -np.abs(I-Imax/np.sqrt(2)))
plt.plot(f, I)
plt.axvline(f0)
plt.axvline(f1)
plt.axvline(f2)

print (f0)
print(f1)
print(f2)

Q1 = f0/(f2-f1)
eQ1 = Q1* np.sqrt( (ef/f0)**2 + (np.sqrt(2)*ef/(f2-f1))**2 )

_, f01, f11, f21 = strombreite(f, I+0.005*0.7)
_, f02, f12, f22 = strombreite(f, I-0.005*0.7)

Q11 = f01/(f21-f11)
Q12 = f02/(f22-f12)


### Breite Phasenverschiebung

def phasenbreite(f, phi):
    i = np.argmax(-np.abs(phi))
    f0 = f[i]
    
    f1 = f[ np.argmax( -np.abs(phi-45) ) ]
    f2 = f[ np.argmax( -np.abs(phi+45) ) ]
    return f0, f1, f2, i

f0, f1, f2, i = phasenbreite(f, phi)

plt.figure(2)
plt.plot(f, phi)
plt.plot(f, np.concatenate((-np.abs(phi[:i]-45), -np.abs(phi[i:]+45))))
plt.axvline(f0)
plt.axvline(f1)
plt.axvline(f2)

print(f0)
print(f1)
print(f2)

Q2 = f0/(f2-f1)
eQ2 = Q2* np.sqrt( (ef/f0)**2 + (np.sqrt(2)*ef/(f2-f1))**2 )



### Spannungsüberhöhung

def spannung(f, UL, UC):
    i = np.argmax(-abs(UL-UC))
    U_max = ((UL+UC)/2)[i]
    f0 = f[i]
    
    return U_max, f0

U_max, f0 = spannung(f, UL, UC)

U0 = np.mean(U)

eU0 = np.std(U, ddof=1) *3
eU_max = eU0

plt.figure(3)
plt.plot(f, UL)
plt.plot(f, UC)
plt.axhline(U_max)
plt.axvline(f0)

Q3 = U_max/U0
eQ3 = Q3 * np.sqrt( (eU_max/U_max)**2 + (eU0/U0)**2 )


U_max, _ = spannung(f, UL+0.01*UL+0.005*7, UC+0.01*UC+0.005*7)
Q31 = U_max/(U0)#+0.01*U0+0.005*7)

U_max, _ = spannung(f, UL-0.01*UL-0.005*7, UC-0.01*UC-0.005*7)
Q32 = U_max/(U0)#-0.01*U0-0.005*7)



plt.figure(4)
plt.errorbar(f, I, fmt=".")
plt.title("{0:s} Ohm Widerstand - Gesamtstrom".format(widerstand))
plt.xlabel("f / Hz")
plt.ylabel("I / A")


plt.figure(5)
plt.errorbar(f, UL, fmt=".")
plt.errorbar(f, UC, fmt=".")
plt.title("{0:s} Ohm Widerstand - Spannung L und C".format(widerstand))
plt.xlabel("f / Hz")
plt.ylabel("U / V")
plt.figtext(0.22, 0.67, "$U_C$")
plt.figtext(0.35, 0.28, "$U_L$")


plt.figure(6)
plt.errorbar(f, phi, fmt=".")
plt.title("{0:s} Ohm Widerstand - Phase".format(widerstand))
plt.xlabel("f / Hz")
plt.ylabel("$\phi$ / Grad")
