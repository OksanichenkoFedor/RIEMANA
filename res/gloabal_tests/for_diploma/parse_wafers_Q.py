from res.gloabal_tests.for_diploma.funks import parce_wafer
import os
from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np


files = os.listdir("../../data/Test_Q")
good_files = []
Qs = []
for file in files:
    if file[-4:]==".zip":
        good_files.append(file)
        Q = int(84.0 / (int(file.split("_")[-1][5:-4])))
        Qs.append(Q)

Qs, good_files = zip(*[(b, a) for b, a in sorted(zip(Qs, good_files))])
print(Qs)
print(good_files)
fig, axises = plt.subplots(3, 3, figsize=(13, 11))
#parce_wafer("../data/test_Q/"+good_files[0], axises[0][0])
DepthX = []
DepthY = []
for i in trange(len(good_files)):
    Q = int(84.0/(int(good_files[i].split("_")[-1][5:-4])))
    ind1 = i%3
    ind2 = i//3
    _, delta_x, delta_y = parce_wafer("../../data/test_Q/"+good_files[i], axises[ind2][ind1])
    DepthX.append(delta_x)
    DepthY.append(delta_y)
    axises[ind2][ind1].set_title("Q="+str(Q),size=20)





plt.show()
fig, [ax1, ax2, ax3] = plt.subplots(1, 3, figsize=(12, 6))
ax1.plot(Qs[:len(DepthY)], DepthY)
ax1.set_ylabel(r"$V_y,\frac{A}{\text{мин}}$", size=15)
ax1.set_xlabel("Q", size=10)
ax1.set_ylim([0, 1.1*max(DepthY)])
ax1.set_title("(a)", y=-0.15, loc='left', size=20)
ax1.grid()

ax2.plot(Qs[:len(DepthX)], np.array(DepthY)/np.array(DepthX))
ax2.set_ylabel(r"$\frac{V_y}{V_x}$", size=15)
ax2.set_xlabel("Q", size=10)
ax2.set_ylim([0, 1.1*max(np.array(DepthY)/np.array(DepthX))])
ax2.set_title("(b)", y=-0.15, loc='left', size=20)
ax2.grid()


ax3.plot(Qs[:len(DepthX)], DepthX)
ax3.set_ylabel(r"$V_x,\frac{A}{\text{мин}}$", size=15)
ax3.set_xlabel("Q", size=10)
ax3.set_ylim([0, 1.1*max(DepthX)])
ax3.set_title("(c)", y=-0.15, loc='left', size=20)
ax3.grid()

plt.show()
