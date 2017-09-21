# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:20:04 2017

@author: morit
"""
import Histogramme as h
import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import scipy.optimize as opt
import scipy.odr as odr

messing = h.get_werte('weiss')
T = messing[0]+273.
Terr = messing[3]
U = messing[2]

def func(x,a,b,c):
    return a+b*(x**(c))
def dfunc(x,a,b,c):
    return b*c*x**(c-1.)

def chifunc((a,b,c)):
    chisq = np.sum(((U - func(T,a,b,c))/Terr)**2)
    return chisq

def anpassung(T, U,sigT,sigU):
    plt.plot(T,U)
    popt,pcov = opt.curve_fit(func,T,U,sigma=np.sqrt(sigT**2+(dfunc*sigU)**2),absolute_sigma=True,p0 = [0.,1e-10,4.],maxfev = 5000)
    xwerte = np.linspace(T[0],T[-1],1000)
    ywerte = func(xwerte,*popt)
    plt.plot(xwerte,ywerte)
    print popt
    
def minimierung(T,Terr,U):
    
    result =  opt.minimize(chifunc,[0.,1e-9,4.])
    print result

startwerte_weiss = []
startwerte_schwarz = []
startwerte_messing = []
startwerte_spiegel = []

def regression(T, U,sigT,sigU):
    def f(B, T):
        return B[0]+B[1]*(T**(B[2]))

    model  = odr.Model(f)
    data   = odr.RealData(T, U, sx=sigT, sy=sigU)
    anpassung    = odr.ODR(data, model, beta0=[-13,1.37e-10,4.],maxit = 50000000)
    output = anpassung.run()
    ndof = len(T)-3
    chiq = output.res_var
    corr = output.cov_beta[0,1]/np.sqrt(output.cov_beta[0,0]*output.cov_beta[1,1])

    return output.beta[0],output.sd_beta[0],output.beta[1],output.sd_beta[1],output.beta[2],output.sd_beta[2],chiq,corr

def main():
    messing = h.get_werte('spiegel')
    T = messing[0]+273.
    Terr = messing[1]
    U = messing[2]
    Uerr = messing[3]
    #anpassung(T,U,Terr,Uerr)
    #minimierung(T,Terr,U)
    a,ea,b,eb,c,ec,chi,cov =  regression(T,U,Terr,Uerr)
    ax1=plt.subplot(211)
    plt.errorbar(T,U,yerr = Uerr, xerr = Terr,linestyle='None',marker='.')
    plt.ylabel('U in V')
    xwerte = np.linspace(T[0],T[-1],1000)
    ywerte = func(xwerte,a,b,c)
    plt.plot(xwerte,ywerte)
    plt.figtext(0.2,0.7,'a={0:.3g}$\pm${1:.3g} \n m={2:.3g}$\pm${3:.3g} \n n={4:.3g}$\pm${5:.3g} \n $\chi^2$/ndof={6:.3g}'
                .format(a,ea,b,eb,c,ec,chi))
    ax2=plt.subplot(212,sharex=ax1)
    plt.xlabel('T in K')
    plt.ylabel('Residuen')
    plt.errorbar(T,U-func(T,a,b,c),yerr=np.sqrt(Uerr**2 +(dfunc(T,a,b,c)*Terr)**2),linestyle='None',marker='.')
    plt.axhline(y=0,linestyle='dashed')
    plt.show()
    #umrechnung: p0 = p0*




if __name__ == "__main__":
    main()