from numba import njit
import numpy as np

from res.getero.algorithm.dynamic_profile import give_coords_from_num


@njit()
def check_collision(vec1, angle, curr_segment):
    x1, y1 = vec1[0], vec1[1]
    x3, y3 = curr_segment[0, 0], curr_segment[0, 1]
    x4, y4 = curr_segment[1, 0], curr_segment[1, 1]
    x2 = x1 + np.sin(angle)
    y2 = y1 + np.cos(angle)
    div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if div == 0:
        # прямая и луч параллельны друг другу
        return False, np.zeros(2), 0.0
    x_cross = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / div
    y_cross = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / div

    if (x_cross - x4) * (x_cross - x3) + (y_cross - y4) * (y_cross - y3) > 0 or (x_cross - x1) * (x2 - x1) + (
            y_cross - y1) * (y2 - y1) <= 0:
        # пересечение вне отрезка
        return False, np.zeros(2), 0.0
    else:
        # пересечение на отрезке
        # print(x3, y3, x4, y4, x_cross, y_cross)
        cross_vec = np.zeros(2)
        cross_vec[0], cross_vec[1] = x_cross, y_cross
        return True, cross_vec, count_norm_angle(x3, y3, x4, y4)


@njit()
def count_norm_angle(x1, y1, x2, y2):
    # Пустота всегда слева от линии поэтому мы всегда явно можем определить угол от нормали.
    # Он будет улгом вектора ребра + 90.
    delta_x, delta_y = x2 - x1, y2 - y1
    cos = delta_y / np.sqrt(delta_x * delta_x + delta_y * delta_y)
    sin = delta_x / np.sqrt(delta_x * delta_x + delta_y * delta_y)
    if cos >= 0 and sin >= 0:
        # первая четверть
        angle = np.arccos(cos)
    elif cos < 0 and sin >= 0:
        # вторая четверть
        angle = np.pi - np.arcsin(sin)
    elif cos < 0 and sin < 0:
        # третья четверть
        angle = np.pi + np.arccos((-1.0) * cos)
    elif cos >= 0 and sin < 0:
        # четвёртая четверть
        angle = (-1.0) * np.arccos(cos)
    angle = angle + np.pi * 0.5
    return angle

@njit()
def check_rect_collision(vec0, angle, left, right, up, down):
    x0, y0 = vec0[0], vec0[1]
    #up - перевёрнутый это минимальная координата на самом деле
    delta_x1 = np.sin(angle)
    delta_y1 = np.cos(angle)
    val1 = count_vec_mult(delta_x1, delta_y1, right - x0, up - y0)
    val2 = count_vec_mult(delta_x1, delta_y1, right - x0, down - y0)
    val3 = count_vec_mult(delta_x1, delta_y1, left - x0, down - y0)
    val4 = count_vec_mult(delta_x1, delta_y1, left - x0, up - y0)
    return (val1 * val2 <= 0 or val3 * val4 <= 0) or val2*val3<=0

@njit()
def count_vec_mult(delta_x1, delta_y1, delta_x2, delta_y2):
    return delta_x1*delta_y2-delta_x2*delta_y1

@njit()
def count_curr_collision_cell(cross_vec, curr_segment):
    part = (cross_vec - curr_segment[0])/(curr_segment[1]-curr_segment[0])
    if (curr_segment[1]-curr_segment[0])[0]!=0:
        res_part=part[0]
    else:
        res_part=part[1]
    if np.abs(part[0]-part[1])>10**(-5) and ((curr_segment[1]-curr_segment[0])[0]!=0 and (curr_segment[1]-curr_segment[0])[1]!=0):
        print("Мы не на отрезке: ", cross_vec, curr_segment, part)
    if res_part<0.5:
        return curr_segment[0]-0.5
    else:
        return curr_segment[1]-0.5

@njit()
def count_curr_prev_att(cross_vec, curr_segment, fall_angle, border_arr):
    #print("start count_curr_prev_att: ", cross_vec, curr_segment, fall_angle)
    curr_point = count_curr_collision_cell(cross_vec, curr_segment)
    curr_att_x, curr_att_y = int(curr_point[0]), int(curr_point[1])
    angle = count_norm_angle(curr_segment[0,0], curr_segment[0,1], curr_segment[1,0], curr_segment[1,1]) - np.pi*0.5

    if angle<0:
        angle+=2*np.pi
    #print("count angle: ", angle / np.pi)
    curr_f_num = 4.0*(angle/np.pi)
    if curr_f_num<0:
        curr_f_num+=8

    curr_f_num = int(curr_f_num)
    unfound = True
    #print("start find prev_att x,y")
    while unfound:
        prev_att_x, prev_att_y = give_coords_from_num(curr_f_num, curr_att_x, curr_att_y)
        if (prev_att_x < border_arr.shape[0] and prev_att_x >= 0) and (
                prev_att_y < border_arr.shape[1] and prev_att_y >= 0):
            if border_arr[prev_att_x, prev_att_y, 0] == -1:
                unfound = False
            else:
                curr_f_num = int(curr_f_num - 1)
                if curr_f_num < 0:
                    curr_f_num = int(curr_f_num + 8.0)
        else:
            #print("Мы на краю находимся ", prev_att_x, prev_att_y, border_arr.shape)
            curr_f_num = int(curr_f_num - 1)
            if curr_f_num < 0:
                curr_f_num = int(curr_f_num + 8.0)


    #print("end count_curr_prev_att: ", curr_att_x, curr_att_y, prev_att_x, prev_att_y)
    return curr_att_x, curr_att_y, prev_att_x, prev_att_y, curr_f_num
