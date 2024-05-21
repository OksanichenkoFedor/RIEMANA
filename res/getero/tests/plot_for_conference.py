import matplotlib.pyplot as plt
import numpy as np


def plot(cX, cY, label, color):
    delta_X = np.ones(cX.shape) * 0.0
    delta_Y = np.ones(cY.shape) * 25.0

    XY = cX * cY
    X2 = cX * cX
    Y2 = cY * cY
    c_k = (XY.mean() - (cX.mean()) * (cY.mean())) / (X2.mean() - cX.mean() ** 2)
    c_b = cY.mean() - c_k * (cX.mean())
    deltaK = ((len(cX) * 1.0) ** (-0.5)) * (
                ((Y2.mean() - cY.mean() ** 2) / ((X2.mean()) - cX.mean() ** 2) - c_k ** 2) ** 0.5)
    deltaB = deltaK * ((X2.mean() - cX.mean() ** 2) ** 0.5)
    print(label)
    print("k = " + str(round(c_k * 60, 3)) + " +- " + str(round(deltaK * 60, 3)))
    print("b = " + str(round(c_b, 3)) + " +- " + str(round(deltaB, 3)))

    def f_full(x, k, b):
        return (k * x + b)


    plt.errorbar(cX, cY, xerr=delta_X, yerr=delta_Y, fmt='o', markersize="2", elinewidth=1, color=color)
    plt.plot(cX, f_full(cX, c_k, c_b), linewidth=1.0, color=color, label=label)

plt.figure(figsize=(7, 8))
plot(np.load("../../data/data_bez_h_L/timesU200_Ar0.1.npy"), np.load("../../data/data_bez_h_L/depthsU200_Ar0.1.npy"), "10% Ar", "b")
plot(np.load("../../data/data_bez_h_L/timesU200_Ar0.1.npy"), np.load("../../data/data_bez_h_L/depthsU200_Ar0.5.npy"), "50% Ar", "r")
plot(np.load("../../data/data_bez_h_L/timesU200_Ar0.1.npy"), np.load("../../data/data_bez_h_L/depthsU200_Ar0.9.npy"), "90% Ar", "g")
plt.ylabel("Глубина травления, ангстрем", size=15)
plt.xlabel("Время, с", size=15)
plt.suptitle('Зависимость грубины травления от времени', size=15)
plt.grid()
plt.legend()
plt.show()
