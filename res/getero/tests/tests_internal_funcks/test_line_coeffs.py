from pickletools import bytes1

import numpy as np
import matplotlib.pyplot as plt

from res.getero.algorithm.ray_tracing.profile_approximation import give_coefs_line


#veber = np.array([2.1, 2.8, 3.45, 4.05, 5.0, 5.35, 5.95, 6.4, 7.05, 7.45, 7.65, 7.9, 8.05, 8.2, 6.5])#Веберы,вычесть 2
#current = np.array([0.01, 0.15, 0.27, 0.38, 0.56, 0.63, 0.76, 0.85, 1.0, 1.11, 1.21, 1.32, 1.42, 1.50, 0.89])#Амперыplt.plot(current, veber)
#plt.plot(veber, current)
#give_coefs_line(veber, current)
#plt.show()

def convert(cstr):
    cstr = cstr[1:-1].split()
    for i in range(len(cstr)):
        cstr[i] = float(cstr[i])
    return np.array(cstr)
bX1, bY1 = convert("[3.5 3.5 3.5 4.5 5.5 6.5]"), convert("[5.5 6.5 7.5 8.5 8.5 8.5]")

#bX1, bY1 = np.array([1,2,3,4,5]), np.array([1,2,3,4,5])
bX2, bY2 = convert("[9.5 10.5 11.5 12.5 12.5 12.5]"), convert("[8.5 8.5 8.5 7.5 6.5 5.5]")
print(bX1, bX2)
w1 = give_coefs_line(bX1, bY1)
w2 = give_coefs_line(bX2, bY2)
print(w1, w2)
#print(give_coefs_line(bX1-3.5, bY1-5.5), give_coefs_line(bX1+2, bY1))




fig, ax = plt.subplots(figsize=(15, 10))
ax.set_aspect(1)
ax.set_ylim([max(bY1.max(),bY2.max())+1, min(bY1.min(),bY2.min())-1])
x_ticks = np.arange(min(bX1.min(),bX2.min()), max(bX1.max(),bX2.max()), 1)
y_ticks = np.arange(min(bY1.min(),bY2.min()), max(bY1.max(),bY2.max()), 1)
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)
ax.grid()
ax.plot(bX1, bY1, color="b")
ax.plot(bX2, bY2, color="b")
plt.show()