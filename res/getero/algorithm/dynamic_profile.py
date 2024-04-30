from numba import njit
import numpy as np


@njit()
def delete_point(border_layer_arr, curr_x, curr_y):
    prev_x, prev_y, next_x, next_y = border_layer_arr[curr_x, curr_y][1:]
    if np.abs(prev_x - curr_x) + np.abs(prev_y - curr_y) == 0:
        print("prev: ", prev_x - curr_x, prev_y - curr_y)
    elif np.abs(next_x - curr_x) + np.abs(next_y - curr_y) == 0:
        print("next: ", next_x - curr_x, next_y - curr_y)
    prev_num = give_num_in_circle(prev_x - curr_x, prev_y - curr_y)
    next_num = give_num_in_circle(next_x - curr_x, next_y - curr_y)
    if prev_num == next_num:
        print("Замкнутый цикл!!! Плохо!")
    i = (prev_num + 1) % 8
    unfound_exit = True
    while i != next_num and unfound_exit:
        x, y = give_coords_from_num(i, curr_x, curr_y)
        if border_layer_arr[x, y, 0] == -1:
            unfound_exit = False
        i = (i + 1) % 8
    if unfound_exit:
        # выход находится после next
        # идём по часовой, там внутренность
        add = +1
    else:
        # выход находится после prev
        # идём против часовой, там внутренность
        add = -1
    i = (prev_num + add) % 8
    tmp_prev_x, tmp_prev_y = prev_x, prev_y
    while i != next_num:
        x, y = give_coords_from_num(i, curr_x, curr_y)
        if i % 2 == 0 and border_layer_arr[x, y, 0] != 1:
            border_layer_arr[tmp_prev_x, tmp_prev_y, 3] = x
            border_layer_arr[tmp_prev_x, tmp_prev_y, 4] = y
            border_layer_arr[x, y, 1] = tmp_prev_x
            border_layer_arr[x, y, 2] = tmp_prev_y
            border_layer_arr[x, y, 0] = 1
            tmp_prev_x, tmp_prev_y = x, y
        i = (i + add) % 8
    border_layer_arr[tmp_prev_x, tmp_prev_y, 3] = next_x
    border_layer_arr[tmp_prev_x, tmp_prev_y, 4] = next_y
    border_layer_arr[next_x, next_y, 1] = tmp_prev_x
    border_layer_arr[next_x, next_y, 2] = tmp_prev_y

    border_layer_arr[curr_x, curr_y] = [-1, -1, -1, -1, -1]


@njit()
def give_num_in_circle(delta_x, delta_y):
    if np.abs(delta_x) > 1:
        delta_x = delta_x / np.abs(delta_x)
    if np.abs(delta_y) > 1:
        delta_y = delta_y / np.abs(delta_y)
    ans = delta_x * delta_y * delta_x * delta_y
    if delta_y == 1 and delta_x > -1:
        return ans + 0
    if delta_x == 1 and delta_y < 1:
        return ans + 2
    if delta_y == -1 and delta_x < 1:
        return ans + 4
    if delta_x == -1 and delta_y > -1:
        return ans + 6


@njit()
def give_coords_from_num(num, start_x, start_y):
    if num % 8 == 0:
        x, y = 0, 1
    if num % 8 == 1:
        x, y = 1, 1
    if num % 8 == 2:
        x, y = 1, 0
    if num % 8 == 3:
        x, y = 1, -1
    if num % 8 == 4:
        x, y = 0, -1
    if num % 8 == 5:
        x, y = -1, -1
    if num % 8 == 6:
        x, y = -1, 0
    if num % 8 == 7:
        x, y = -1, 1
    return x + start_x, y + start_y


def give_line_arrays(border_layer, prev_x, prev_y, next_x, next_y, curr_x, curr_y, size=1):
    x, y = prev_x, prev_y
    X = []
    Y = []
    while x != next_x or y != next_y:
        X.append((x - curr_x + 1.5) * size)
        Y.append((y - curr_y + 1.5) * size)
        x, y = border_layer[x, y, 3], border_layer[x, y, 4]
    X.append((x - curr_x + 1.5) * size)
    Y.append((y - curr_y + 1.5) * size)
    return X, Y
