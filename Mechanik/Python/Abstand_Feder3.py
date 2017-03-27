# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:01:07 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def get_zeros(t,U,index_output=True):
    '''
    gibt liste mit Tupeln der Form (t,U,index) zurück,
    dieser index und nächster sind die "nullstellen"
    '''
    zeros=[]
    for i in range(len(U)-1):
        if U[i]>0 and U[i+1]<0:
            zeros.append((t[i],U[i],i))
        elif U[i]<0 and U[i+1]>0:
            zeros.append((t[i],U[i],i))
        elif U[i]==0 and U[i-1] and i>0:
            zeros.append((t[i],U[i],i))
    #don't bother with this stuff
    if index_output==False:
        return zeros
    else:
        index=[]
        for x in zeros:
            index.append((x[2],x[2]+1))
        return index

def get_peaks(x, y):
    zeros = get_zeros(x, y, index_output=False)
    peaks = []
    index = []
    
    for n in range(len(zeros)-1):
        peaks.append(p.peak(x, y, zeros[n][0], zeros[n+1][0]))
    for peak in peaks:
        indx = find_nearest(x, peak)
        if (np.abs(y[indx]) > 0.05*np.mean(np.abs(y[0])) and x[indx] > 0.1):
            index.append(indx)
    index = np.array(index)
    
    return index



#automatisches ienlesen!!
stab=[]
for i in range(5):
    stab.append(p.lese_lab_datei('lab/Feder3/Quadrat/stab'+str(1+i)+'.lab'))

kerben=[]
for i in range(6):    
    kerben.append(p.lese_lab_datei('lab/Feder3/Quadrat/stab'+str(i+1)+'_1.lab'))



plt.figure(2)
plt.plot(kerben[0][:,1],kerben[0][:,2])
plt.xlabel('t[s]')
plt.ylabel('[U[V]]')
plt.title('Spannungsverlauf erste Kerbe')
plt.show()

plt.figure(3)
plt.plot(kerben[2][:,1],kerben[2][:,2])
plt.xlabel('t[s]')
plt.ylabel('U[V]')
plt.title('Spannungsverlauf dritte Kerbe')
plt.show()






#get periods, muss optimiert werden :
def get_period(messung,bedingung=False):
    if bedingung==True:
        periods=[]
        for x in messung:
            t,U=x[:,1][50:-6000],x[:,2][50:-6000]
            peaks=get_peaks(t,U)
            periods.append(2*((t[-1]-t[0])/(len(peaks)-1)))
        return np.mean(periods),np.std(periods,ddof=1)/np.sqrt(len(periods)),np.std(periods,ddof=1)
    else:
        outi=[]
        for i in range(len(kerben)):
            ts,Us=kerben[i][:,1][100:-6500],kerben[i][:,2][100:-6500]
            peakss=get_peaks(ts,Us)
            period=2.0*((ts[peakss[-1]]-ts[peakss[0]]))/(len(peakss)-1)
            outi.append(period)
        return outi


def get_period_alt(messung):
    pass




def verschiebemethode(x,y,xerr,yerr,systx,systy,a,b):
    #verschiebemethide, ruckgabe von syst err a und syst err b
    xp,yp=x+systx,y+systy
    xm,ym=x-systx,y-systy
    apx,eapx,bpx,ebpx,chiqpx,covpx=p.lineare_regression_xy(xp,y,xerr,yerr)
    amx,eamx,bmx,ebmx,chiqmx,covmx=p.lineare_regression_xy(xm,y,xerr,yerr)
    apy,eapy,bpy,ebpy,chiqpy,covpy=p.lineare_regression_xy(x,yp,xerr,yerr)
    amy,eamy,bmy,ebmy,chiqmy,covmy=p.lineare_regression_xy(x,ym,xerr,yerr)
    
    err_ax=np.abs(apx-a)/2+np.abs(amx-a)/2
    err_ay=np.abs(apy-a)/2+np.abs(amy-a)/2
    err_bx=np.abs(bpx-b)/2+np.abs(bmx-b)/2
    err_by=np.abs(bpy-b)/2+np.abs(bmy-b)/2

    err_a=np.sqrt(err_ax**2+err_ay**2)
    err_b=np.sqrt(err_bx**2+err_by**2)
    
    return err_a,err_b


def verschiebemethode_nur_y(x,y,xerr,yerr,systx,a,b):
    xp,xm=x+systx,x-systx
    apx,eapx,bpx,ebpx,chiqpx,covpx=p.lineare_regression_xy(xp,y,xerr,yerr)
    amx,eamx,bmx,ebmx,chiqmx,covmx=p.lineare_regression_xy(xm,y,xerr,yerr)

    err_ax=np.abs(apx-a)/2+np.abs(amx-a)/2
    err_bx=np.abs(bpx-b)/2+np.abs(bmx-b)/2
    
    return err_ax,err_bx



#hier habe ich error eine position vorgezogen
nurstab,error,placeholder=get_period(stab,bedingung=True)
results=get_period(kerben)    

#hier lin reg für D
#kerbenabstand 4.99cm
#kerbenerror=0.1/sqrt(12)

kerben=[(n+1)*4.99*10**(-2) for n in range(6)]
kerben_error=[np.sqrt(n+1)*0.1/np.sqrt(12)*10**(-2) for n in range(6)]
#kerben_error=np.full(6,0.1/np.sqrt(12)*10**(-2))
kerben,kerben_error=np.array(kerben),np.array(kerben_error)
error=np.full(6,error)
results=np.array(results)

#hier fehlertrafo und regression
results2=results**2
kerben2=kerben**2
kerben_error2=2*kerben*kerben_error
error2=2*results*error

a,ea,b,eb,chiq,cov=p.lineare_regression_xy(kerben2,results2,kerben_error2,error2)

#digits
d=3

#hier plot
x=np.arange(0,0.11,0.005)

plt.figure(0)
plt.errorbar(kerben2,results2,yerr=error2,xerr=kerben_error2,linestyle='None')
plt.plot(x,a*x+b)
plt.figtext(0.15,0.7,'a= '+str(np.round(a,d))+'+-'+str(np.round(ea,d))+'\n'+'b= '+str(np.round(b,d))+'+-'+str(np.round(eb,d))+'\n $\chi^2$='+str(np.round((chiq/(len(kerben)-2)),2)))
plt.ylabel('$T^2$[$s^2$]')
plt.xlabel('$r^2$[$m^2$]')
plt.show()

plt.figure(1)
plt.xlabel('t[s]')
plt.ylabel('Residuen')
plt.errorbar(kerben2,results2-(a*kerben2+b),yerr=np.sqrt(error**2+(a*kerben_error2)**2),linestyle='None')
plt.axhline(0,linestyle='dashed')
plt.show()




#heir systematische fehler
T2_syst=np.full(len(kerben2),0)
r2_syst=2*kerben*0.7*10**(-3)

syst_a,syst_b=verschiebemethode(kerben2,results2,kerben_error2,error2,r2_syst,T2_syst,a,b)




print('a= {}+-{}+-{}    b= {}+-{}+-{}').format(np.round(a,d),np.round(ea,d),np.round(syst_a,d),np.round(b,d),np.round(eb,d),np.round(syst_b,d))


