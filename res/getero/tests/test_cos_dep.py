import numpy as np
import matplotlib.pyplot as plt

def generate_cos_point():
    a = 2*np.random.random()-1
    x = np.arcsin(a)
    return x

A = []
num_bins = 100
num_points = 1000000
for i in range(num_points):
    A.append(generate_cos_point())
b = np.arange(-1, 1, 0.01)*np.pi/2
plt.hist(A, bins=100)
plt.plot(b, np.cos(b)*((np.pi*num_points)/(2.0*num_bins)))
plt.show()