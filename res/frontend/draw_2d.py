import numpy as np

import matplotlib.pyplot as plt
import matplotlib.path as mplPath


def draw_contur(points):
    N = 40
    print("Points: ", points.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(points) - 1):
        ax.plot([points[i, 0], points[(i + 1) % len(points), 0]],
                [points[i, 1], points[(i + 1) % len(points), 1]], color=((i * 1.0) / (len(points) - 1.0), 0, 0))
    ax.grid()
    delta_x = np.max(points[:, 0]) - np.min(points[:, 0])
    delta_y = np.max(points[:, 1]) - np.min(points[:, 1])
    x_lim = [np.min(points[:, 0]) - 0.5 * delta_x, np.max(points[:, 0]) + 0.5 * delta_x]
    y_lim = [np.min(points[:, 1]) - 0.5 * delta_y, np.max(points[:, 1]) + 0.5 * delta_y]
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)

    bbPath = mplPath.Path(points)
    arr = np.zeros((N, N))
    x = np.arange(x_lim[0], x_lim[1], (x_lim[1] - x_lim[0]) / (1.0 * N))
    y = np.arange(y_lim[0], y_lim[1], (y_lim[1] - y_lim[0]) / (1.0 * N))
    good_x = []
    good_y = []
    for i in range(N):
        for j in range(N):
            if bbPath.contains_point([x[i], y[j]]):
                #ax.plot(x[i], y[j], 'ro')
                good_x.append(x[i])
                good_y.append(y[j])

    #plt.show()
    return np.array(good_x), np.array(good_y)
