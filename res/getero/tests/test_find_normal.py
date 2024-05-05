import numpy as np

from res.getero.entities.wafer import Wafer
from res.getero.algorithm.dynamic_profile import give_line_arrays
from res.getero.frontend.grafic_funcs import plot_line
from res.getero.algorithm.profile_approximation import give_part_of_border, give_mnk, line_approximationr

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from numba import njit

W = Wafer(0.05, 1)
W.process_file("del6.txt")

X, Y = give_line_arrays(W.border_arr, W.start_x, W.start_y, W.end_x, W.end_y, 0, 0,
                        size=1)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect(1)
for i in range(len(X)):
    # print(X[i], Y[i])
    rect = Rectangle((X[i], Y[i]), 1, 1, color="b")
    ax.add_patch(rect)
ax.set_ylim([W.ysize, 0])
plot_line(ax, X, Y, W.start_x, W.start_y, 0.5, 0.5, do_points=False)


# plt.show()

def give_coefs_2(x, y):
    print(x.shape)
    X = np.ones((x.shape[0], 5))
    X[:, 0] = x * x
    X[:, 1] = x * y
    X[:, 2] = y * y
    X[:, 3] = x
    X[:, 4] = y
    w = np.linalg.pinv(X) @ np.ones((x.shape[0], 1))
    return w

def give_coefs(x, y):
    X = np.ones((x.shape[0], 2))
    X[:, 0] = x
    X[:, 1] = y
    w = np.linalg.pinv(X) @ np.ones((x.shape[0], 1))[:,0]
    return w


def give_coords_2(x, A, B, C, D, E):
    X = []
    Y = []
    for i in range(len(x)):
        det = (E + B * x[i]) ** 2 - 4 * C * (A * x[i] * x[i] + D * x[i] - 1)
        y1 = (-E - B * x[i] + np.sqrt(det)) / (2 * C)
        y2 = (-E - B * x[i] - np.sqrt(det)) / (2 * C)
        X.append(x[i])
        X.append(x[i])
        Y.append(y1)
        Y.append(y2)
    return X, Y

def give_coords(x, A, B):
    return x, (1-A*x)/B





x, y = W.give_el_border(66)

curr_x, curr_y = 78, 42.0
prev_x, prev_y = 80, 40

# curr_x, curr_y = 20, 22
# prev_x, prev_y = 21, 21

test_n(W.border_arr, x, y, 2, curr_x, curr_y, prev_x, prev_y, ax)
plt.show()
