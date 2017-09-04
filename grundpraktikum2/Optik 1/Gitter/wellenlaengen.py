import numpy as np
import matplotlib.pyplot as plt
import Praktikum as p

bogenmass = lambda grad, minuten: 2*np.pi/360 * (grad + minuten/60)

linien = []

for i in range(5):
    # ordnung, grad, min, grad, min
    linien.append(np.genfromtxt("Linie {0}.txt".format(i+1), delimiter=", ", skip_header=2))
    

# Nummer der bearbeiteten Linie
nummer = 1


n = nummer -1
d = 1658.9*1e-9 #1.0/600000
std_d = 1e-9
grad = (linien[n][:,1]+linien[n][:,3])/2
minuten = (linien[n][:,2]+linien[n][:,4])/2

ordnung = linien[n][:,0]*-1
winkel = bogenmass(grad, minuten)
winkel -= winkel[0]
std = np.full(len(winkel), np.sqrt(2)*0.000298)
yerr = np.sqrt((std*d*np.cos(winkel))**2+(std_d*np.sin(winkel))**2)

a, ea, b, eb, chi2 = p.lineare_regression_festes_b(ordnung, d*np.sin(winkel)*1e9, np.full(len(ordnung),0.0), yerr*1e9)
x = np.arange(5)-2
             


plt.figure(1, [6.5,4.5])
plt.subplot2grid((6,1),(0,0), rowspan=4)
plt.errorbar(ordnung, d*np.sin(winkel)*1e9, yerr=yerr*1e9, fmt="o")
plt.plot(x, a*x+b)
plt.figtext(0.2, 0.75, "$\lambda = ({0:3.2f} \pm {1:3.2f})$ nm".format(a, ea))
plt.ylabel("d sin($\\theta$) [nm]")
plt.xlabel("n")

# Residuen
plt.subplot2grid((6,1),(-2,0), rowspan=2)
plt.errorbar(ordnung, d*np.sin(winkel)*1e9-a*ordnung, yerr=yerr*1e9, fmt = ".")
plt.axhline(linestyle="dashed")
plt.ylabel("Residuen [$nm$]")
plt.xlabel("n")


# direkt ausrechnen und mitteln
wellenlaenge = d*np.sin(winkel)/ordnung