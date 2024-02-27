import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def give_sigma(filename):
    f = open(filename)
    A = f.readlines()
    f.close()
    Engs = []
    Sigmas = []
    for line in A:
        line = np.array(line.split()).astype(float)
        Engs.append(line[0])
        Sigmas.append(line[1])
    spl = CubicSpline(Engs, Sigmas)
    return spl
spl1 = give_sigma("res/plasma/reactions_consts/Ar_mom1.txt")
spl2 = give_sigma("res/plasma/reactions_consts/Ar_mom2.txt")
spl3 = give_sigma("res/plasma/reactions_consts/Cl_mom.txt")
engs = np.arange(0,50,0.1)
plt.plot(engs,spl1(engs),label="Ar1")
plt.plot(engs,spl2(engs),label="Ar2")
plt.plot(engs,spl3(engs),label="Cl")
plt.grid()
plt.legend()
plt.show()