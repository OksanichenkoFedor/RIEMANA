import numpy as np
import time

import matplotlib.pyplot as plt
import matplotlib.path as mplPath
from matplotlib.patches import PathPatch

import res.config as config


def draw_contur(points, type):
    N = config.start_number_on_line
    print("Points: ", points.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(points) - 1):
        ax.plot([points[i, 0], points[(i + 1) % len(points), 0]],
                [points[i, 1], points[(i + 1) % len(points), 1]],
                color=((i * 1.0) / (len(points) - 1.0), 1.0 - (i * 1.0) / (len(points) - 1.0), 0))
    ax.grid()
    delta_x = np.max(points[:, 0]) - np.min(points[:, 0])
    delta_y = np.max(points[:, 1]) - np.min(points[:, 1])
    x_lim = [np.min(points[:, 0]) - 0.5 * delta_x, np.max(points[:, 0]) + 0.5 * delta_x]
    y_lim = [np.min(points[:, 1]) - 0.5 * delta_y, np.max(points[:, 1]) + 0.5 * delta_y]
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    print("dfdfdfdfdf")
    bbPath = mplPath.Path(points)
    good_x = []
    good_y = []
    unfound = True
    print("dfdfdfdfdf")
    if type=="cyl":

        plt.show()
    while len(good_x) < config.elem_on_face:
        print(len(good_x),N)
        x = np.arange(x_lim[0], x_lim[1], (x_lim[1] - x_lim[0]) / (1.0 * N))
        Nx = N
        while x.shape[0] > N:
            Nx = Nx - 0.1
            x = np.arange(x_lim[0], x_lim[1], (x_lim[1] - x_lim[0]) / (1.0 * Nx))
        while x.shape[0] < N:
            Nx = Nx + 0.1
            x = np.arange(x_lim[0], x_lim[1], (x_lim[1] - x_lim[0]) / (1.0 * Nx))
        x = np.repeat(x.reshape((N, 1)), N, axis=1).reshape((N * N, 1))
        y = np.arange(y_lim[0], y_lim[1], (y_lim[1] - y_lim[0]) / (1.0 * N))
        Ny = N
        while y.shape[0] > N:
            Ny = Ny - 0.1
            y = np.arange(y_lim[0], y_lim[1], (y_lim[1] - y_lim[0]) / (1.0 * Ny))
        while y.shape[0] < N:
            Ny = Ny + 0.1
            y = np.arange(y_lim[0], y_lim[1], (y_lim[1] - y_lim[0]) / (1.0 * Ny))
        y = (np.repeat(y.reshape((N, 1)), N, axis=1).T).reshape((N * N, 1))
        xy = np.concatenate((x, y), axis=1)

        ans = bbPath.contains_points(list(xy))
        x = xy[:, 0]
        y = xy[:, 1]
        b = ans.astype("int").sum()
        y = np.where(ans, y, "")
        x = np.where(ans, x, "")
        x = x[x != ""].astype(float)
        y = y[y != ""].astype(float)
        good_x = x
        good_y = y
        N = int(N * 1.5)
        if len(good_x) >= config.elem_on_face and unfound:
            unfound = False
            x_lim[0], x_lim[1] = np.min(x)-2*(x_lim[1]-x_lim[0])/N, np.max(x)+2*(x_lim[1]-x_lim[0])/N
            y_lim[0], y_lim[1] = np.min(y)-2*(y_lim[1]-y_lim[0])/N, np.max(y)+2*(y_lim[1]-y_lim[0])/N
            good_x = []
            good_y = []
            N = config.start_number_on_line
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
    for i in range(len(good_x)):
        plt.plot(good_x[i], good_y[i], ".", color="r")
    ax.add_patch(PathPatch(bbPath, facecolor='g', lw=2, fill=False))
    print("dfdfdfdfdf")
    #plt.show()
    return np.array(good_x), np.array(good_y), bbPath


def give_angle(x, y, r):
    cos = x / r
    sin = y / r
    cos = cos / np.sqrt(cos * cos + sin * sin)
    sin = sin / np.sqrt(cos * cos + sin * sin)
    if x * x + y * y < 0.0001*r*r:
        return 0
    elif cos >= 0 and sin >= 0:
        return np.arcsin(sin)
    elif cos >= 0 and sin < 0:
        return 2 * np.pi - np.arcsin((-1) * sin)
    elif cos < 0 and sin >= 0:
        return np.pi - np.arcsin(sin)
    elif cos < 0 and sin < 0:
        return np.pi + np.arcsin((-1) * sin)
    else:
        print("Aхтунг!!!gfgfgfgfg ",x,y,r)
