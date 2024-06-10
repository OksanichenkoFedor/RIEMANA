


import numpy as np
import matplotlib.pyplot as plt

from res.getero.algorithm.utils import generate_cos_point
import matplotlib as mpl
#mpl.rcParams.update(mpl.rcParamsDefault)
print("000000000000000000000000000000000000")
#mpl.rcParams['text.usetex'] = True
#mpl.rcParams["text.latex.preamble"]  = r"\usepackage{cmbright}"
print("000000000000000000000000000000000000")


A = []
num_bins = 100
num_points = 100000
for i in range(num_points):
    A.append(generate_cos_point())
b = np.arange(-1, 1, 0.01)*np.pi/2
plt.figure(figsize=(10,7))
print("000000000000000000000000000000000000")
plt.hist(A, bins=100, label=r"Пакет радикалов $Cl$")
print("000000000000000000000000000000000000")
plt.plot(b, np.abs(np.sin(b))*((np.pi*num_points)/(2.0*num_bins)),label=r"$\frac{\pi cos(\varphi)n_{\text{пиков}}}{N}$")
plt.xlabel(r"$\varphi$", size=15)
plt.ylabel(r"Количество частиц в диапазоне $0.01\pi$")
plt.legend()
plt.show()