import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

bogenmass = lambda grad, minuten: 2*np.pi/360 * (grad + minuten/60)

linien = []

for i in range(5):
    # ordnung, grad, min, grad, min
    linien.append(np.genfromtxt("Linie {0}.txt".format(i+1), delimiter=", ", skip_header=2))
    

# Nummer der bearbeiteten Linie
nummer = 2


n = nummer -1
d = 1658.91*1e-9 #1.0/600000
std_d = 0.3424e-9
grad = (linien[n][:,1]+linien[n][:,3])/2
minuten = (linien[n][:,2]+linien[n][:,4])/2

korrektur = -0.94

ordnung = linien[n][1:,0]*-1
winkel = bogenmass(grad, minuten)
print winkel[0]
winkel[0]=bogenmass(84.,33.)
print winkel[0]
winkel -= winkel[0]
winkel = winkel[1:]
std = np.full(len(winkel), 0.000298)
yerr = np.sqrt((std*d*np.cos(winkel-bogenmass(korrektur,0)))**2+(std_d*np.sin(winkel-bogenmass(korrektur,0)))**2)



a, ea, chi2 = p.lineare_regression_festes_b(ordnung, d*(np.sin(bogenmass(korrektur,0.0))+np.sin(winkel-bogenmass(korrektur,0.0)) )*1e9, np.full(len(winkel),1e-20), yerr*1e9)
x = np.arange(5)-2
             


plt.figure(1, [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(ordnung, d*(np.sin(bogenmass(korrektur,0))+np.sin(winkel-bogenmass(korrektur,0)) )*1e9, yerr=yerr*1e9, fmt="o")
plt.plot(x, a*x)
plt.figtext(0.2, 0.7, "$\lambda = ({0:3.2f} \pm {1:3.2f})$ nm\n$\chi^2/ndof$ = {2:3.2f}\n$\\varphi = -1^\\circ$".format(a, ea, chi2/3))
plt.ylabel("d[sin($\\varphi$)+sin($\\theta-\\varphi$)] [nm]")
plt.xlabel("n")

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(ordnung, d*(np.sin(bogenmass(korrektur,0))+np.sin(winkel-bogenmass(korrektur,0)) )*1e9-a*ordnung, yerr=yerr*1e9, fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [$nm$]")
plt.xlabel("n")

sys = std_d/d * a
literatur = np.array([404.66, 435.83, 546.07, 576.96, 579.07])
abw = (a-literatur[n])/np.sqrt(sys**2+ea**2)

# direkt ausrechnen und mitteln
# Nullte Ordnung
theta_0 = bogenmass(84,(35+53)/2)

grad = np.array([ linien[n][1:,1], linien[n][1:,3] ])
minuten = np.array([ linien[n][1:,2], linien[n][1:,4] ])
ordnung = np.array([ linien[n][1:,0] , linien[n][1:,0] ])

winkel = theta_0 - bogenmass(grad, minuten)
std_stat = 0.000298

wellenlaenge = d * (np.sin(bogenmass(korrektur, 0)) + np.sin(winkel-bogenmass(korrektur,0))) / ordnung
sig_stat = d * np.cos(winkel-bogenmass(korrektur,0))/np.abs(ordnung) * std_stat
sig_sys = (np.sin(bogenmass(korrektur,0))+np.sin(winkel-bogenmass(korrektur,0)))/ordnung * std_d
mittelwert = np.mean(wellenlaenge.flatten()) * 1e9
std = np.std(wellenlaenge.flatten(), ddof=1) * 1e9
std_sys = np.mean(sig_sys.flatten()) * 1e9

                 
lam = d*( np.sin(np.mean(winkel[:,0])-bogenmass(korrektur,0)) - np.sin(np.mean(winkel[:,1])-bogenmass(korrektur,0)) )/2e-9
stat = d/2e-9*np.sqrt( np.cos(np.mean(winkel[:,0])-bogenmass(korrektur,0))**2*std_stat**2 + np.cos(np.mean(winkel[:,1])-bogenmass(korrektur,0))**2*std_stat**2  )

 