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
    #print(prev_num, next_num)
    if prev_num == next_num:
        # предыдущий и следующий на одной линии
        simple_delition(border_layer_arr, curr_x, curr_y, -1)
        return 0
    i = (prev_num + 1) % 8
    unfound_exit = True
    while i != next_num and unfound_exit:
        x, y = give_coords_from_num(i, curr_x, curr_y)
        if border_layer_arr[x, y, 0] == -1:
            unfound_exit = False
        i = (i + 1) % 8
    #print("unfound_exit: ",unfound_exit)
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
    unfound_connector = True
    while i != next_num:
        #print(i)
        x, y = give_coords_from_num(i, curr_x, curr_y)
        if i % 2 == 0 and border_layer_arr[x, y, 0] == 0:
            unfound_connector = False
            border_layer_arr[tmp_prev_x, tmp_prev_y, 3] = x
            border_layer_arr[tmp_prev_x, tmp_prev_y, 4] = y
            border_layer_arr[x, y, 1] = tmp_prev_x
            border_layer_arr[x, y, 2] = tmp_prev_y
            border_layer_arr[x, y, 0] = 1
            tmp_prev_x, tmp_prev_y = x, y
        i = (i + add) % 8
    if unfound_connector:
        #print("проверяем другие возможности")
        add = -add
        i = (prev_num + add) % 8
        tmp_prev_x, tmp_prev_y = prev_x, prev_y
        while i != next_num:
            #print(i)
            x, y = give_coords_from_num(i, curr_x, curr_y)
            if i % 2 == 0 and border_layer_arr[x, y, 0] == 0:
                #print("->")
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


@njit()
def create_point(border_layer_arr, curr_x, curr_y, next_x, next_y):
    border_layer_arr[curr_x, curr_y, 0] = 1
    if not check_if_inside(border_layer_arr, next_x, next_y):
        # проверка на то, что мы не закрываем более старую клетку границы
        if curr_x > 0:
            if check_if_inside(border_layer_arr, curr_x - 1, curr_y):
                next_x, next_y = curr_x - 1, curr_y
        if curr_x < border_layer_arr.shape[0] - 1:
            if check_if_inside(border_layer_arr, curr_x + 1, curr_y):
                next_x, next_y = curr_x + 1, curr_y
        if curr_y > 0:
            if check_if_inside(border_layer_arr, curr_x, curr_y - 1):
                next_x, next_y = curr_x, curr_y - 1
        if curr_y < border_layer_arr.shape[1] - 1:
            if check_if_inside(border_layer_arr, curr_x, curr_y + 1):
                next_x, next_y = curr_x, curr_y + 1
    #print("next: ",next_x,next_y)
    old_prev_x, old_prev_y = border_layer_arr[next_x, next_y, 1], border_layer_arr[next_x, next_y, 2]
    old_next_x, old_next_y = border_layer_arr[next_x, next_y, 3], border_layer_arr[next_x, next_y, 4]
    delta_prev = (old_prev_x - curr_x) * (old_prev_x - curr_x) + (old_prev_y - curr_y) * (old_prev_y - curr_y)
    delta_next = (old_next_x - curr_x) * (old_next_x - curr_x) + (old_next_y - curr_y) * (old_next_y - curr_y)
    # цепляем новую точку
    if delta_prev > delta_next:
        #print("a")
        # цепляем новую за текущий
        simple_addition_after(border_layer_arr, next_x, next_y, curr_x, curr_y)
    else:
        #print("b")
        #print(old_prev_x, old_prev_y)
        #print(curr_x, curr_y)
        # цепляем новую за предыдущий
        simple_addition_after(border_layer_arr, old_prev_x, old_prev_y, curr_x, curr_y)



    # производим удаление внутренних клеток границы

    # назад
    prev_x, prev_y = border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2]
    while check_if_inside(border_layer_arr, prev_x, prev_y):
        simple_delition(border_layer_arr, prev_x, prev_y, 0)
        prev_x, prev_y = border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2]
    # вперёд
    next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    while check_if_inside(border_layer_arr, next_x, next_y):
        simple_delition(border_layer_arr, next_x, next_y, 0)
        next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]


@njit()
def simple_delition(border_layer_arr, curr_x, curr_y, type):
    prev_x, prev_y = border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2]
    next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4] = next_x, next_y
    border_layer_arr[next_x, next_y, 1], border_layer_arr[next_x, next_y, 2] = prev_x, prev_y
    border_layer_arr[curr_x, curr_y] = [type, -1, -1, -1, -1]

@njit()
def simple_addition_after(border_layer_arr, prev_x, prev_y, curr_x, curr_y):
    next_x, next_y = border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4]
    border_layer_arr[curr_x, curr_y, 0] = 1

    border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2] = prev_x, prev_y
    border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4] = curr_x, curr_y

    border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4] = next_x, next_y
    border_layer_arr[next_x, next_y, 1], border_layer_arr[next_x, next_y, 2] = curr_x, curr_y


@njit()
def check_if_inside(border_layer_arr, curr_x, curr_y):
    is_inside = True
    if border_layer_arr[curr_x, curr_y, 0]==-1:
        return False
    if curr_x > 0:
        if border_layer_arr[curr_x - 1, curr_y, 0] == -1:
            is_inside = False
    if curr_x < border_layer_arr.shape[0] - 1:
        if border_layer_arr[curr_x + 1, curr_y, 0] == -1:
            is_inside = False
    if curr_y > 0:
        if border_layer_arr[curr_x, curr_y - 1, 0] == -1:
            is_inside = False
    if curr_y < border_layer_arr.shape[1] - 1:
        if border_layer_arr[curr_x, curr_y + 1, 0] == -1:
            is_inside = False
    return is_inside


def give_line_arrays(border_layer, prev_x, prev_y, next_x, next_y, curr_x, curr_y, size=1):
    x, y = prev_x, prev_y
    X = []
    Y = []
    while x != next_x or y != next_y:
        X.append(x)
        Y.append(y)
        x, y = border_layer[x, y, 3], border_layer[x, y, 4]
    X.append((x) * size)
    Y.append((y) * size)
    return X, Y

def give_max_y(border_layer, prev_x, prev_y, next_x, next_y):
    x, y = prev_x, prev_y
    y_max = y
    while x != next_x or y != next_y:
        y_max = max(y,y_max)
        x, y = border_layer[x, y, 3], border_layer[x, y, 4]
    return y_max

