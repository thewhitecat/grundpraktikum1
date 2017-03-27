# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 18:03:48 2014

Useful tools for Grundpraktikum Physik, based on MAPLE sheet Praktikum.mws

@author: henning
"""

import numpy as np
from numpy import sqrt,sin,cos,log,exp
import scipy
import scipy.fftpack
import scipy.odr
import StringIO

def lese_lab_datei(dateiname):
    '''
    CASSY LAB Datei einlesen.

    Messdaten werden anhand von Tabulatoren identifiziert.

    Gibt ein numpy-Array zurueck.

    '''
    f = open(dateiname)
    dataSectionStarted = False
    dataSectionEnded = False
    data = ''
    for line in f:
        if '\t' in line and not dataSectionEnded:
            data += line
            dataSectionStarted = True
        if not '\t' in line and dataSectionStarted:
            dataSectionEnded = True
    f.close()
    return np.genfromtxt(StringIO.StringIO(data))


def lineare_regression(x,y,ey):
    '''

    Lineare Regression.

    Parameters
    ----------
    x : array_like
        x-Werte der Datenpunkte
    y : array_like
        y-Werte der Datenpunkte
    ey : array_like
        Fehler auf die y-Werte der Datenpunkte

    Diese Funktion benoetigt als Argumente drei Listen:
    x-Werte, y-Werte sowie eine mit den Fehlern der y-Werte.
    Sie fittet eine Gerade an die Werte und gibt die
    Steigung a und y-Achsenverschiebung b mit Fehlern
    sowie das chi^2 und die Korrelation von a und b
    als Liste aus in der Reihenfolge
    [a, ea, b, eb, chiq, cov].
    '''

    s   = sum(1./ey**2)
    sx  = sum(x/ey**2)
    sy  = sum(y/ey**2)
    sxx = sum(x**2/ey**2)
    sxy = sum(x*y/ey**2)
    delta = s*sxx-sx*sx
    b   = (sxx*sy-sx*sxy)/delta
    a   = (s*sxy-sx*sy)/delta
    eb  = sqrt(sxx/delta)
    ea  = sqrt(s/delta)
    cov = -sx/delta
    corr = cov/(ea*eb)
    chiq  = sum(((y-(a*x+b))/ey)**2)

    return(a,ea,b,eb,chiq,corr)


def lineare_regression_xy(x,y,ex,ey):
    '''

    Lineare Regression mit Fehlern in x und y.

    Parameters
    ----------
    x : array_like
        x-Werte der Datenpunkte
    y : array_like
        y-Werte der Datenpunkte
    ex : array_like
        Fehler auf die x-Werte der Datenpunkte
    ey : array_like
        Fehler auf die y-Werte der Datenpunkte

    Diese Funktion benoetigt als Argumente vier Listen:
    x-Werte, y-Werte sowie jeweils eine mit den Fehlern der x-
    und y-Werte.
    Sie fittet eine Gerade an die Werte und gibt die
    Steigung a und y-Achsenverschiebung b mit Fehlern
    sowie das chi^2 und die Korrelation von a und b
    als Liste aus in der Reihenfolge
    [a, ea, b, eb, chiq, cov].

    Die Funktion verwendet den ODR-Algorithmus von scipy.
    '''
    a_ini,ea_ini,b_ini,eb_ini,chiq_ini,corr_ini = lineare_regression(x,y,ey)

    def f(B, x):
        return B[0]*x + B[1]

    model  = scipy.odr.Model(f)
    data   = scipy.odr.RealData(x, y, sx=ex, sy=ey)
    odr    = scipy.odr.ODR(data, model, beta0=[a_ini, b_ini])
    output = odr.run()
    ndof = len(x)-2
    chiq = output.res_var*ndof
    corr = output.cov_beta[0,1]/np.sqrt(output.cov_beta[0,0]*output.cov_beta[1,1])

    return output.beta[0],output.sd_beta[0],output.beta[1],output.sd_beta[1],chiq,corr


def fourier(t,y):
    '''

    Fourier-Transformation.

    Parameters
    ----------
    t : array_like
        Zeitwerte der Datenpunkte
    y : array_like
        y-Werte der Datenpunkte

    Gibt das Fourierspektrum in Form zweier Listen (freq,amp)
    zurueck, die die Fourieramplituden als Funktion der zugehoerigen
    Frequenzen enthalten.
    '''

    dt = (t[-1]-t[0])/(len(t)-1)
    fmax = 0.5/dt
    step = fmax/len(t)
    freq=np.arange(0.,fmax,2.*step)
    amp = np.zeros(len(freq))
    i=0
    for f in freq:
        omega=2.*np.pi*f
        sc = sum(y*cos(omega*t))/len(t)
        ss = sum(y*sin(omega*t))/len(t)
        amp[i] = sqrt(sc**2+ss**2)
        i+=1
    return (freq,amp)


def fourier_fft(t,y):
    '''

    Schnelle Fourier-Transformation.

    Parameters
    ----------
    t : array_like
        Zeitwerte der Datenpunkte
    y : array_like
        y-Werte der Datenpunkte

    Gibt das Fourierspektrum in Form zweier Listen (freq,amp)
    zurueck, die die Fourieramplituden als Funktion der zugehoerigen
    Frequenzen enthalten.
    '''
    dt = (t[-1]-t[0])/(len(t)-1)
    amp = abs(scipy.fftpack.fft(y))
    freq = scipy.fftpack.fftfreq(t.size,dt)
    return (freq,amp)


def exp_einhuellende(t,y,ey,Sens=0.1):
    '''
    Exponentielle Einhuellende.

    Parameters
    ----------
    t : array_like
        Zeitwerte der Datenpunkte
    y : array_like
        y-Werte der Datenpunkte
    ey : array_like
        Fehler auf die y-Werte der Datenpunkte
    Sens : float, optional
        Sensitivitaet, Wert zwischen 0 und 1

    Die Funktion gibt auf der Basis der drei Argumente (Listen
    mit t- bzw. dazugehoerigen y-Werten plus y-Fehler) der Kurve die
    Parameter A0 und delta samt Fehlern der Einhuellenden von der Form
    A=A0*exp(-delta*t) (Abfallende Exponentialfunktion) als Liste
    [A0, sigmaA0, delta, sigmaDelta] aus.
    Optional kann eine Sensibilitaet angegeben werden, die bestimmt,
    bis zu welchem Prozentsatz des hoechsten Peaks der Kurve
    noch Peaks fuer die Berechnung beruecksichtigt werden (default=10%).
    '''
    if not 0.<Sens<1.:
        raise ValueError('Sensibilitaet muss zwischen 0 und 1 liegen!')

    # Erstelle Liste mit ALLEN Peaks der Kurve
    Peaks=[]
    PeakZeiten=[]
    PeakFehler=[]
    GutePeaks=[]
    GutePeakZeiten=[]
    GutePeakFehler=[]
    if y[0]>y[1]:
        Peaks.append(y[0])
        PeakZeiten.append(t[0])
        PeakFehler.append(ey[0])
    for i in range(1,len(t)-1):
        if y[i] >= y[i+1] and \
           y[i] >= y[i-1] and \
           ( len(Peaks)==0 or y[i] != Peaks[-1] ): #handle case "plateau on top of peak"
           Peaks.append(y[i])
           PeakZeiten.append(t[i])
           PeakFehler.append(ey[i])

    # Loesche alle Elemente die unter der Sensibilitaetsschwelle liegen
    Schwelle=max(Peaks)*Sens
    for i in range(0,len(Peaks)):
        if Peaks[i] > Schwelle:
            GutePeaks.append(Peaks[i])
            GutePeakZeiten.append(PeakZeiten[i])
            GutePeakFehler.append(PeakFehler[i])

    # Transformiere das Problem in ein lineares
    PeaksLogarithmiert = log(np.array(GutePeaks))
    FortgepflanzteFehler = np.array(GutePeakFehler) / np.array(GutePeaks)
    LR = lineare_regression(np.array(GutePeakZeiten),PeaksLogarithmiert,FortgepflanzteFehler)

    A0=exp(LR[2])
    sigmaA0=LR[3]*exp(LR[2])
    delta=-LR[0]
    sigmaDelta=LR[1]
    return(A0,sigmaA0,delta,sigmaDelta)

def untermenge_daten(x,y,x0,x1):
    '''
    Extrahiere kleinere Datensaetze aus (x,y), so dass x0 <= x <= x1
    '''
    xn=[]
    yn=[]
    for i,v in enumerate(x):
        if x0<=v<=x1:
            xn.append(x[i])
            yn.append(y[i])

    return (np.array(xn),np.array(yn))

def peak(x,y,x0,x1):
    '''
    Approximiere ein lokales Maximum in den Daten (x,y) zwischen x0 und x1.
    '''
    N = len(x)
    ymin = max(y)
    ymax = min(y)
    i1 = 0
    i2 = N-1
    for i in range(N):
       if x[i]>=x0:
         i1=i
         break
    for i in range(N):
       if x[i]>=x1:
         i2=i+1
         break
    for i in range(i1,i2):
      if y[i]>ymax:
          ymax=y[i]
      if y[i]<ymin:
          ymin=y[i]

    sum_y   = sum(y[i1:i2])
    sum_xy  = sum(x[i1:i2]*y[i1:i2])
    xm = sum_xy/sum_y
    return xm

def peakfinder_schwerpunkt(x,y):
    '''
    Finde Peak in den Daten (x,y).
    '''
    N = len(x)
    val = 1./sqrt(2.)
    i0=0
    i1=N-1
    ymax=max(y)
    for i in range(N):
        if y[i]>ymax*val:
            i0=i
            break
    for i in range(i0+1,N):
        if y[i]<ymax*val:
            i1=i
            break
    xpeak = peak(x,y,x[i0],x[i1])
    return xpeak


def gewichtetes_mittel(y,ey):
    '''
    Berechnet den gewichteten Mittelwert der gegebenen Daten.

    Parameters
    ----------
    y : array_like
        Datenpunkte
    ey : array_like
        Zugehoerige Messunsicherheiten.

    Gibt den gewichteten Mittelwert samt Fehler zurueck.
    '''
    w = 1/ey**2
    s = sum(w*y)
    wsum = sum(w)
    xm = s/wsum
    sx = sqrt(1./wsum)

    return (xm,sx)


