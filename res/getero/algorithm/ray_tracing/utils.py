import numpy as np
from numba import njit

from res.getero.algorithm.dynamic_profile import give_start


@njit()
def give_edges(border_layer_arr):
    x_start, y_start = give_start(border_layer_arr)
    curr_x, curr_y = x_start, y_start
    num_edges = 0
    while border_layer_arr[curr_x, curr_y, 3] != -1 or border_layer_arr[curr_x, curr_y, 4] != -1:
        num_edges += 1
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    Edges = np.zeros((num_edges, 6))
    # строим массив из ячеек будет 6 точек (x1, x2, y1, y2, xm, ym)
    # print(num_edges1, num_edges)
    curr_x, curr_y = x_start, y_start
    for i in range(num_edges):
        Edges[i, 0], Edges[i, 1] = curr_x, border_layer_arr[curr_x, curr_y, 3]
        Edges[i, 2], Edges[i, 3] = curr_y, border_layer_arr[curr_x, curr_y, 4]
        curr_x, curr_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    Edges[:, 4] = 0.5 * (Edges[:, 0] + Edges[:, 1])
    Edges[:, 5] = 0.5 * (Edges[:, 2] + Edges[:, 3])
    return Edges

@njit()
def count_vec_mult(delta_x1, delta_y1, delta_x2, delta_y2):
    return delta_x1*delta_y2-delta_x2*delta_y1