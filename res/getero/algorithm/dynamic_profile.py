#from numba import njit
from res.getero.ray_tracing.cell_by_cell.collision_functions import particle_on_wall
from res.getero.ray_tracing.cell_by_cell.space_orientation import give_next_cell
from res.getero.ray_tracing.utils import count_angle
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def delete_point(border_layer_arr, is_full_arr, is_hard, add_segments, curr_x, curr_y):
    #print("start del")

    prev_x, prev_y, next_x, next_y = border_layer_arr[curr_x, curr_y][1:]
    #print(prev_x, prev_y, next_x, next_y)
    if (prev_x==-1 and prev_y==-1):
        #print("Мы на краю! Слева")

        new_start_x, new_start_y = give_coords_from_num(0, curr_x, curr_y)
        if new_start_x == next_x and new_start_y == next_y:
            #print("Мы попали 2!")
            border_layer_arr[next_x, next_y, 1:3] = [-1, -1]
            border_layer_arr[curr_x, curr_y] = [-1, -1, -1, -1, -1]
            return add_segments
        border_layer_arr[new_start_x, new_start_y] = [1, -1, -1, curr_x, curr_y]
        border_layer_arr[curr_x, curr_y, 1:3] = [new_start_x, new_start_y]

    if (next_x==-1 and next_y==-1):
        #print("Мы на краю! Справа")

        new_end_x, new_end_y = give_coords_from_num(0, curr_x, curr_y)
        if new_end_x == prev_x and new_end_y == prev_y:
            #print("Мы попали 1!")
            border_layer_arr[prev_x, prev_y, 3:] = [-1,-1]
            border_layer_arr[curr_x, curr_y] = [-1, -1, -1, -1, -1]
            return add_segments
        border_layer_arr[prev_x, prev_y, 3:]=[new_end_x, new_end_y]
        border_layer_arr[new_end_x, new_end_y] = [1, curr_x, curr_y, -1, -1]
        border_layer_arr[curr_x, curr_y, 3:] = [new_end_x, new_end_y]

    prev_x, prev_y, next_x, next_y = border_layer_arr[curr_x, curr_y][1:]
    #

    if np.abs(prev_x - curr_x) + np.abs(prev_y - curr_y) == 0:

        print("prev: ", prev_x - curr_x, prev_x - curr_y)
        print(curr_x, curr_y, prev_x, prev_y)
    elif np.abs(next_x - curr_x) + np.abs(next_y - curr_y) == 0:
        print("next: ", next_x - curr_x, next_y - curr_y)
    prev_num = give_num_in_circle(prev_x - curr_x, prev_y - curr_y)
    next_num = give_num_in_circle(next_x - curr_x, next_y - curr_y)

    if prev_num == next_num:
        dpx, dpy, dnx, dny = prev_x - curr_x, prev_y - curr_y, next_x - curr_x, next_y - curr_y
        # предыдущий и следующий на одной линии
        if dpy==0 and dny==0:
            add_segments = simple_delition(border_layer_arr, is_full_arr, is_hard, add_segments, curr_x, curr_y, -1)
            return add_segments
        if (1.0*dpx)/(1.0*dpy)==(1.0*dnx)/(1.0*dny):
            add_segments = simple_delition(border_layer_arr, is_full_arr, is_hard, add_segments, curr_x, curr_y, -1)
            return add_segments
    border_layer_arr[curr_x, curr_y] = [-1, -1, -1, -1, -1]
    add = 1
    # мы ВСЕГДА обходим по часовой

    i = (prev_num + add) % 8
    tmp_prev_x, tmp_prev_y = prev_x, prev_y
    unfound_connector = True
    while i != next_num:
        #print(i)
        x, y = give_coords_from_num(i, curr_x, curr_y)
        if (i % 2 == 0 and border_layer_arr[x, y, 0] == 0) and ( (x>=0 and y>=0) and (x<border_layer_arr.shape[0] and y<border_layer_arr.shape[1]) ):
            unfound_connector = False
            border_layer_arr[x, y, 0] = 1
            add_segments = connection(border_layer_arr, is_full_arr, is_hard, add_segments, tmp_prev_x, tmp_prev_y, curr_x, curr_y, x, y)
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
            if  (i % 2 == 0 and border_layer_arr[x, y, 0] == 0) and ( (x>=0 and y>=0) and (x<border_layer_arr.shape[0] and y<border_layer_arr.shape[1]) ):
                #print("->")
                border_layer_arr[x, y, 0] = 1
                add_segments = connection(border_layer_arr, is_full_arr, is_hard, add_segments, tmp_prev_x, tmp_prev_y, curr_x, curr_y, x, y)
                tmp_prev_x, tmp_prev_y = x, y
            i = (i + add) % 8

    add_segments = connection(border_layer_arr, is_full_arr, is_hard, add_segments, tmp_prev_x, tmp_prev_y, curr_x, curr_y, next_x, next_y)
    #print("end del")
    return add_segments


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def create_point(border_layer_arr, is_full_arr, is_hard, add_segments, curr_x, curr_y, next_x, next_y):
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
        add_segments = simple_delition(border_layer_arr, is_full_arr, is_hard, add_segments, prev_x, prev_y, 0)
        prev_x, prev_y = border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2]
    # вперёд
    next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    while check_if_inside(border_layer_arr, next_x, next_y):
        add_segments = simple_delition(border_layer_arr, is_full_arr, is_hard, add_segments, next_x, next_y, 0)
        next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    return add_segments


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def simple_delition(border_layer_arr, is_full_arr, is_hard, add_segments, curr_x, curr_y, type):
    prev_x, prev_y = border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2]
    next_x, next_y = border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4]
    add_segments = connection(border_layer_arr, is_full_arr, is_hard, add_segments, prev_x, prev_y, curr_x, curr_y, next_x, next_y)
    border_layer_arr[curr_x, curr_y] = [type, -1, -1, -1, -1]
    return add_segments


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def connection(border_layer_arr, is_full_arr, is_hard, add_segments, prev_x, prev_y, curr_x, curr_y, next_x, next_y):
    border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4] = next_x, next_y
    border_layer_arr[next_x, next_y, 1], border_layer_arr[next_x, next_y, 2] = prev_x, prev_y
    # проверяем промежуточные точки
    add_segments = check_void_line_points(prev_x, prev_y, curr_x, curr_y, border_layer_arr, is_full_arr, is_hard,
                                          add_segments, False)
    add_segments = check_void_line_points(curr_x, curr_y, next_x, next_y, border_layer_arr, is_full_arr, is_hard,
                                          add_segments, False)
    add_segments = check_void_line_points(prev_x, prev_y, next_x, next_y, border_layer_arr, is_full_arr, is_hard,
                                          add_segments, True)
    return add_segments

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def simple_addition_after(border_layer_arr, prev_x, prev_y, curr_x, curr_y):
    next_x, next_y = border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4]
    border_layer_arr[curr_x, curr_y, 0] = 1

    border_layer_arr[curr_x, curr_y, 1], border_layer_arr[curr_x, curr_y, 2] = prev_x, prev_y
    border_layer_arr[prev_x, prev_y, 3], border_layer_arr[prev_x, prev_y, 4] = curr_x, curr_y

    border_layer_arr[curr_x, curr_y, 3], border_layer_arr[curr_x, curr_y, 4] = next_x, next_y
    border_layer_arr[next_x, next_y, 1], border_layer_arr[next_x, next_y, 2] = curr_x, curr_y


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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


def give_line_arrays(border_layer, plot_refl_wall):
    X = []
    Y = []
    x, y = give_start(border_layer)
    #print("fff3gla")
    unfound = True
    #print(border_layer.shape)
    while unfound:
        X.append(int(x))
        Y.append(int(y))
        #print(x,y, border_layer[x, y])
        new_x, new_y = border_layer[x, y, 3], border_layer[x, y, 4]
        if new_x==-1 and new_y==-1:
            unfound = False
        else:
            x, y = new_x, new_y

    if plot_refl_wall:
        X.append(int(x) + 0.5)
        Y.append(int(y))
        X.append(int(x) + 0.5)
        Y.append(0)
    return X, Y

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def give_start(border_layer):
    unfound = True
    x, y = 0, 0
    while unfound and y < border_layer.shape[1]:
        if border_layer[x, y, 0] == 1:
            unfound = False
        else:
            y += 1
    if unfound:
        raise Exception("Не найдена левая граница")
    return x, y

def give_end(border_layer):
    unfound = True
    x, y = border_layer.shape[0]-1, 0
    while unfound and y < border_layer.shape[1]:
        if border_layer[x, y, 0] == 1:
            unfound = False
        else:
            y += 1
    if unfound:
        raise Exception("Не найдена правая граница")
    return x, y

def give_max_y(border_layer):
    x, y = give_start(border_layer)
    y_max = y
    unfound = True
    while unfound:
        y_max = max(y, y_max)
        x, y = border_layer[x, y, 3], border_layer[x, y, 4]
        if x==-1 and y==-1:
            unfound = False
    return y_max

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def find_close_void(border_layer_arr, curr_x, curr_y):
    num = 0
    unfound = True
    while unfound:
        new_x, new_y = give_coords_from_num(num, curr_x, curr_y)
        if border_layer_arr[new_x,new_y,0]==0:
            unfound = False
        num+=1
    return new_x, new_y

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_void_line_points(start_x, start_y, end_x, end_y, border_arr, is_full, is_hard, add_segments, do_create):
    #print("start cvlp")
    #print("start: ", start_x, start_y, end_x, end_y)
    if (start_x==-1 or start_y==-1) or (end_x==-1 or end_y==-1):
        print("Incorrect connection dynamic_profile/check_void_line_points: ", start_x, start_y, end_x, end_y)
    inc_x, inc_y = np.sign(end_x - start_x), np.sign(end_y - start_y)
    if np.abs(end_x - start_x) == np.abs(end_y - start_y):
        for i in range(1,np.abs(end_x - start_x)):
            curr_att_x, curr_att_y = start_x + inc_x * i, start_y + inc_y * i
            add_segments = process_void_line_point(curr_att_x, curr_att_y, border_arr, is_full, is_hard, add_segments,
                                                   do_create, start_x, start_y, end_x, end_y)
    else:
        angle = count_angle(end_y - start_y, end_x - start_x)

        #print(angle/np.pi)
        add_segments = process_void_line_point(start_x, start_y, border_arr, is_full, is_hard, add_segments,
                                               do_create, start_x, start_y, end_x, end_y)
        curr_vec = np.zeros(2)
        curr_vec[0], curr_vec[1] = start_x+0.5, start_y+0.5
        new_vec, curr_att_x, curr_att_y = particle_on_wall(start_x, start_y, curr_vec, angle)
        curr_x, curr_y = new_vec[0], new_vec[1]

        #print(curr_att_x, curr_att_y)
        add_segments = process_void_line_point(curr_att_x, curr_att_y, border_arr, is_full, is_hard, add_segments,
                                               do_create, start_x, start_y, end_x, end_y)
        if int(curr_x) - curr_x == 0:
            is_on_horiz = 0
        else:
            is_on_horiz = 1
        while (curr_att_x - end_x != 0) or (curr_att_y - end_y != 0):
            # print("---")
            curr_x, curr_y, is_on_horiz = give_next_cell(curr_x, curr_y, angle, is_on_horiz)
            if is_on_horiz:
                curr_att_y += inc_y
            else:
                curr_att_x += inc_x
            #print(curr_att_x, curr_att_y)
            add_segments = process_void_line_point(curr_att_x, curr_att_y, border_arr, is_full, is_hard, add_segments,
                                                   do_create, start_x, start_y, end_x, end_y)
    return add_segments

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_void_line_point(curr_att_x, curr_att_y, border_arr, is_full, is_hard, add_segments, do_create, start_x, start_y, end_x, end_y):
    #print("start pvlp: ", curr_att_x, curr_att_y)
    #print(border_arr[curr_att_x, curr_att_y], is_full[curr_att_x, curr_att_y])
    if border_arr[curr_att_x, curr_att_y, 0] == -1:
        if is_full[curr_att_x, curr_att_y] == -1:
            if do_create:
                print("Already line point dynamic_profile")
            else:
                pass
                is_full[curr_att_x, curr_att_y] = 0
                border_arr[curr_att_x, curr_att_y, 1:] = [-1, -1, -1, -1]
        else:
            if do_create:
                is_full[curr_att_x, curr_att_y] = -1
                border_arr[curr_att_x, curr_att_y, 1:] = [start_x, start_y, end_x, end_y]
    return add_segments