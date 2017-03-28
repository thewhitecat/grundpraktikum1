# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:42:01 2017

@author: Tim
"""

import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p
import auswertung_nur_Methoden as aus


d=4.99*10**(-2)
edstat=0.1/np.sqrt(12)*10**(-2)
edsyst=0.07*10**(-2)
masse=0.1305
emassestat=0.1/np.sqrt(12)*10**(-3)
emassesyst=0.1*10**(-3)
exsyst=0.1
Direk=0.0218067
eDirekstat=2.514*10**(-4)
eDireksyst=2.940*10**(-4)
eDirektotal=np.sqrt(eDirekstat**2+eDireksyst**2)/10


def get_data():
    data=[]
    for j in range(6):
        appi=[]
        for i in range(4):
            app=p.lese_lab_datei('lab/Feder3/steiner/'+str(j+1)+'verschoben0'+str(i+1)+'.lab')
            appi.append(app)
        data.append(appi)
    return data

#data[kerbe-1][messung-1]

def Steiner(data):
    
    kerben_zeiten,kerben_spannungen=[],[]
    for x in data:
        out1,out2=[],[]
        for i in range(4):
            out1.append(x[i][:,1])
            out2.append(x[i][:,2])
        kerben_zeiten.append(out1)
        kerben_spannungen.append(out2)
   
    perioden=[]
    perioden_error=[]
    for k in range(len(kerben_zeiten)):
        
        times,volts=kerben_zeiten[k],kerben_spannungen[k]
        vor_perioden=[]
        for u in range(len(times)):
            t,U=times[u],volts[u]
            peaks=aus.get_peaks(t,U)
            T=2*(t[peaks[-1]]-t[peaks[0]])/(len(peaks)-1)
            vor_perioden.append(T)
            
        perioden.append(np.mean(vor_perioden))
        perioden_error.append(np.std(vor_perioden,ddof=1)/np.mean(vor_perioden))

    return perioden,perioden_error,np.full(len(perioden),0)
    
'''        
    #habe jetzt perioden und error auf diese
    #jetzt kommz trägheit bestimmen
    J=[]
    eJ=[]
    eJsyst=[]
    for i in range(len(perioden)):
        out1=1/(4*np.pi**2)*Direk*perioden[i]**2
        out2=1/(4*np.pi**2)*Direk*2*perioden[i]*perioden_error[i]
        out3=1/(4*np.pi**2)*eDirektotal*perioden[i]**2
        J.append(out1)
        eJ.append(out2)
        eJsyst.append(out3)
        
    return J,eJ,eJsyst
'''
#rückgabe von J und stat error

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


################################
data=get_data()

#print Steiner(data)
#regressionen etc
#J,eJstat,eJsyst=Steiner(data)
T,eTstat,eTsyst=Steiner(data)
a,eastat,easyst=[],[],[]
for i in range(6):
    a.append((i+1)*d)
    eastat.append(np.sqrt(i+1)*edstat)
    easyst.append((i+1)*edsyst)
    
a2=np.array(a)**2
ea2stat=2*np.array(a)*np.array(eastat)
ea2syst=2*np.array(a)*np.array(easyst)

T2=np.array(T)**2
eT2stat=2*np.array(T)*np.array(eTstat)

m,em,b,eb,chiq,cov=p.lineare_regression_xy(a2,np.array(T2),ea2stat,np.array(eT2stat))    


#mal plotten
digits=5
x=np.linspace(0,0.1,400)
plt.figure(1)
plt.subplot2grid((6,1),(0,0),rowspan=4)
plt.errorbar(a2,T2,xerr=ea2stat,yerr=eT2stat,linestyle='None',fmt='.')
plt.xlabel('$a^2$[$s^2$]')
plt.ylabel('$T^2$[$s^2$]')
plt.plot(x,m*x+b)
plt.figtext(0.2,0.75,'a={}+-{}+-{} \n b={}+-{}+-{} \n $\chi^2/ndof$={}'.format(np.round(m,digits),np.round(em,digits),7.06964,np.round(b,digits),np.round(eb,digits),0.00006,np.round(chiq/(len(T2)-2),digits)))
plt.subplot2grid((6,1),(-2,0),rowspan=2)
plt.axhline(0,linestyle='dashed')
plt.ylabel('Residuen')
plt.xlabel('$a^2$[$m^2$]')
plt.errorbar(a2,T2-m*a2-b,yerr=np.sqrt(eT2stat**2+m**2*ea2stat**2),linestyle='None',fmt='.')
plt.show()

#systematische fehler krallen...
#

systm,systb=verschiebemethode(a2,np.array(T2),ea2stat,np.array(eT2stat),ea2syst,np.array(eTsyst),m,b)

print 'a={}+-{}+-{}'.format(np.round(m,digits),np.round(em,digits),np.round(systm,digits))
print 'b={}+-{}+-{}'.format(np.round(b,digits),np.round(eb,digits),np.round(systb,digits))
print '----------------'


