import numpy as np
from matplotlib import pyplot as plt

from res.getero.algorithm.dynamic_profile import give_line_arrays
from res.global_entities.wafer import Wafer


def plot_wafer(c_wafer):
    X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
    X, Y = X[326:333], Y[326:333]
    print(X)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect(1)
    ax.set_ylim([0.5*(np.array(Y).max()-np.array(Y).min())+np.array(Y).max(), np.array(Y).min()-0.5*(np.array(Y).max()-np.array(Y).min())])
    ax.set_xlim([0.5*(np.array(X).max()-np.array(X).min())+np.array(X).min(), np.array(X).max()-0.5*(np.array(X).max()-np.array(X).min())])
    x_ticks = np.arange(np.array(X).min(), np.array(X).max(), 1)+0.5
    y_ticks = np.arange(np.array(Y).min(), np.array(Y).max(), 1)+0.5
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid()

    ax.plot(X, Y)
    return ax

end_wafer = Wafer()
end_wafer.load("../files/test_create_intersection.zip")
plot_wafer(end_wafer)
print(end_wafer.check_self_intersection())
plt.show()