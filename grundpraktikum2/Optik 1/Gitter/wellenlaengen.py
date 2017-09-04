import numpy as np
import matplotlib.pyplot as plt

bogenmass = lambda grad, minuten: 2*np.pi/360 * (grad + minuten/60)

nue = []

for i in range(5):
    nue.append(np.genfromtxt("Linie{1}.txt".format(i), skip_header=2))
