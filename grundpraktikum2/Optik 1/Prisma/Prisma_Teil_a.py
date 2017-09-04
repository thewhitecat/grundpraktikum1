# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 13:53:01 2017

@author: Tim
"""

import numpy as np
import Praktikum
import matplotlib.pyplot as plt
import scipy.odr as odr

def degtorad((degree,minute)):
    decimal=minute/60.0
    degree=degree+decimal
    return degree/180.0*np.pi

#rauschmessung
#508.58nm
raw_data_rauschen=[(25,3),(25,1),(25,0),(25,1),(25,1),(25,3),(25,9),(25,3),(25,10),(25,20),(25,14),(25,11),(25,9),(25,8),(25,10)]
andere_seite=[(147,21),(147,22),(147,13),(147,11),(147,16)]
data_rauschen=[]
for x in raw_data_rauschen:
    data_rauschen.append(degtorad(x))
data_rauschen=np.array(data_rauschen)
mean_rauschen=np.mean(data_rauschen)
std_rauschen=np.std(data_rauschen,ddof=1)

#werte in rad

#print mean_rauschen
#print std_rauschen

def auswertung(raw_data1,raw_data2):
    data1=[]
    for x in raw_data1:
        data1.append(degtorad(x))
    data1=np.array(data1)
    
    data2=[]
    for x in raw_data2:
        data2.append(degtorad(x))
    data2=np.array(data2)
    
    psi_1=np.mean(data1)
    psi_2=np.mean(data2)
    
    psi_err_1=std_rauschen/np.sqrt(len(data1))
    psi_err_2=std_rauschen/np.sqrt(len(data2))
    
    delta=(psi_2-psi_1)/2
    delta_err=np.sqrt(psi_err_1**2+psi_err_2**2)/2
    
    return delta,delta_err
    

'''
hier daten der messung
'''

#643,85nm
data_643_1=[(27,20),(27,20),(27,24)]
data_643_2=[(144,57),(144,55),(144,59)]
d_643,ed_643=auswertung(data_643_1,data_643_2)

#579,07nm
data_579_1=[(26,34),(26,32),(26,33)]
data_579_2=[(145,48),(145,44),(145,44)]
d_579,ed_579=auswertung(data_579_1,data_579_2)

#546,07nm
data_564_1=[(25,53),(25,54),(25,54)]
data_564_2=[(146,24),(146,25),(146,22)]
d_564,ed_564=auswertung(data_564_1,data_564_2)

#479,99nm
data_479_1=[(24,22),(24,24),(24,18)]
data_479_2=[(147,56),(148,0),(148,2)]
d_479,ed_479=auswertung(data_479_1,data_479_2)

#467,81nm
data_476_1=[(23,55),(23,54),(23,57)]
data_476_2=[(148,22),(148,24),(148,20)]
d_476,ed_476=auswertung(data_476_1,data_476_2)

#435,83nm
data_435_1=[(22,43),(22,45),(22,42)]
data_435_2=[(149,34),(149,33),(149,33)]
d_435,ed_435=auswertung(data_435_1,data_435_2)

#404,66nm
data_404_1=[(21,2),(21,0),(20,56)]
data_404_2=[(151,15),(151,14),(151,18)]
d_404,ed_404=auswertung(data_404_1,data_404_2)


'''
delta werte, aufsteigend von kleinem lambda zu großem lambda
'''

delta=np.array([d_404,d_435,d_476,d_479,d_564,d_579,d_643])
error_delta=np.array([ed_404,ed_435,ed_476,ed_479,ed_564,ed_579,ed_643])

n=np.sin(delta/2.0+30.0/180.0*np.pi)/np.sin(30.0/180.0*np.pi)
en=abs(np.cos(delta/2.0+30.0/180.0*np.pi)/np.sin(30.0/180.0*np.pi)*delta/2.0)*error_delta

l=np.array([404.66,435.83,467.81,479.99,546.07,579.07,643.85])


'''
plots
'''

plt.plot(0)
plt.errorbar(l,n,en,marker='o')
plt.xlim(400,650)
plt.ylim(1.7,1.8)
plt.xlabel('$\lambda / {nm}$')
plt.ylabel('n')
plt.show()

plt.plot(1)
x=1/l**2
plt.errorbar(x,n,en,linestyle='None')
plt.xlim(0.0000020,0.0000063)
plt.ylim(1.7,1.8)
plt.xlabel('$\lambda^{-2} / {nm}^{-2}$')
plt.ylabel('n')
plt.xticks(rotation=20)


a,ea,b,eb,chiq,cov=Praktikum.lineare_regression(x,n,en)
test=np.linspace(0.0000020,0.0000063)
plt.plot(test,a*test+b)
chiq_ndof=chiq/(len(n)-2)
print 'chiq/ndof ='+str(round(chiq_ndof,4))


plt.figtext(0.2,0.7,'a={}+-{} \n b={}+-{} \n Chi^2/ndof={}'.format(round(a,3),round(ea,3),round(b,4),round(eb,4),round(chiq_ndof,3)))


plt.show()


'''
def f(par,x):
    return par[0]*(1+par[1]*x)

function = odr.Model(f)
mydata = odr.RealData(x,n,sy=en)
myodr = odr.ODR(mydata,function,beta0=[2,7000])
myoutput = myodr.run()
myoutput.pprint()



par=myoutput.beta
epar=myoutput.sd_beta
#chiq=myoutput.sum_sqare
#chiq_ndof=chiq/(len(n)-3)

test=np.linspace(0.0000020,0.0000063)
plt.plot(test,f(par,test))
plt.show()
'''








