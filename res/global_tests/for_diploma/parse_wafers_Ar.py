from res.global_tests.for_diploma.funks import parce_wafer
import os
from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np


files = os.listdir("../../data/Ar_change")
print("fdfdfdfdf")
good_files = []
Y_Ars = []
for file in files:
    if file[-4:]==".zip":
        good_files.append(file)
        #Q = int(84.0 / (int(file.split("_")[-1][5:-4])))
        Y_Ars.append(round(float(file.split("_")[2][2:]),2))
Y_Ars, good_files = zip(*[(b, a) for b, a in sorted(zip(Y_Ars, good_files))])
print(Y_Ars)
print(good_files)
fig, axises = plt.subplots(4, 5, figsize=(13, 11))
#parce_wafer("../data/test_Q/"+good_files[0], axises[0][0])
DepthX = []
DepthY = []
for i in trange(len(good_files)):

    ind1 = i%5
    ind2 = i//5
    _, delta_x, delta_y = parce_wafer("../../data/Ar_change/"+good_files[i], axises[ind2][ind1], x_cut=60, y_end=220)
    DepthX.append(delta_x)
    DepthY.append(delta_y)
    axises[ind2][ind1].set_title(r"$y_{Ar}$="+str(Y_Ars[i]), size=20)





plt.show()
fig, [ax1, ax2, ax3] = plt.subplots(1, 3, figsize=(18, 6))
ax1.plot(Y_Ars[:len(DepthY)], np.array(DepthY)/3.0)
ax1.set_ylabel(r"$V_y,\frac{A}{\text{мин}}$", size=15)
ax1.set_xlabel(r"$y_{Ar}$", size=10)
ax1.set_ylim([0, 1.1*max(DepthY)/3.0])
ax1.set_title("(a)", y=-0.15, loc='left', size=20)
ax1.grid()

ax2.plot(Y_Ars[:len(DepthX)], np.array(DepthY)/np.array(DepthX))
ax2.set_ylabel(r"$\frac{V_y}{V_x}$", size=15)
ax2.set_xlabel(r"$y_{Ar}$", size=10)
ax2.set_title("(b)", y=-0.15, loc='left', size=20)
ax2.grid()

ax3.plot(Y_Ars[:len(DepthX)], np.array(DepthX)/3.0)
ax3.set_ylabel(r"$V_x,\frac{A}{\text{мин}}$", size=15)
ax3.set_xlabel(r"$y_{Ar}$", size=10)
ax3.set_ylim([0, 1.1*max(DepthX)/3.0])
ax3.set_title("(c)", y=-0.15, loc='left', size=20)
ax3.grid()

plt.show()