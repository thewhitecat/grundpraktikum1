# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 13:59:48 2017

@author: morit
"""
import numpy as np

def bogen(grad,sek):
    zwischen = grad + sek/60.
    return zwischen/360.*2.*np.pi

std =0.00167776357135/np.sqrt(2)
astd = 111.7
bstd = 0.000482
a=14427.608
b=1.686
eps = bogen(60,0)
def napprox(y):
    return a*(1+b1/(y*y)+b2/(y**4))
def delta(x1,x2): 
    return np.abs(x1-x2)/2
def n(delta):
    x = np.sin((delta+eps)/2)
    y = np.sin(eps/2)
    return x/y
#def  lam(a,b,c,n):
#    test = n/(a*c)+b**2/(4*c**2)-1/c**2
#    x = np.sqrt(test)
#    y = b/(2*c)
 #   return np.sqrt(1/(x-y))
def lamlin(a,b,n):
    return np.sqrt(a/(n-b))
def  lam(a,b,c,y):
    zahl = np.sqrt(a)*np.sqrt(a*b**2-4*a*c+4*c*y)+a*b
    nenn = 2*a-2*y
    return np.sqrt(-zahl/nenn)

def nstd(delta):
    x = np.cos((delta+eps)/2)
    y = np.sin(eps/2)
    z = delta/2
    return x/y*z*std

def lamstd(a,b,n,astd,bstd,nstd):
    return np.sqrt(a/(n-b))/(2*a)*astd + a/(2*(n-b)**2*np.sqrt(a/(n-b))) * (nstd + bstd)

    
rot = [[bogen(27,20), bogen(27,16)],[bogen(145,2), bogen(145,3)]]
blau = [[bogen(24,22), bogen(24,21)],[bogen(147,53), bogen(147,24)]]
blauer = [[bogen(24,6), bogen(24,7)],[bogen(148,11), bogen(148,10)]]
blausten = [[bogen(23,59), bogen(23,57)],[bogen(148,20), bogen(148,22)]]
rot1 = np.mean(rot[0])
rot2 = np.mean(rot[1])
rotdelta = delta(np.mean(rot[0]),np.mean(rot[1]))
nrot = n(rotdelta)
nrotstd =nstd(rotdelta)
lamrot= lamlin(14427.608,1.686,nrot)
rotstd = lamstd(a,b,nrot,astd,bstd,nstd(rotdelta))
blau1 = np.mean(blau[0])
blau2= np.mean(blau[1])
blaudelta = delta(blau1,blau2)
nblau = n(blaudelta)
lamblau= lamlin(14427.608,1.686,nblau)
blaustd = lamstd(a,b,nblau,astd,bstd,nstd(blaudelta))
blauer1= np.mean(blauer[0])
blauer2 = np.mean(blauer[1])
blauerdelta = delta(blauer1,blauer2)
nblauer = n(blauerdelta)
lamblauer= lamlin(14427.608,1.686,nblauer)

blausten1= np.mean(blausten[0])
blausten2 = np.mean(blausten[1])
blaustendelta = delta(blausten1,blausten2)
nblausten = n(blaustendelta)
lamblausten= lamlin(14427.608,1.686,nblausten)