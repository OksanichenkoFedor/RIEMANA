import numpy as np

from res.getero.algorithm.dynamic_profile import give_coords_from_num
from res.getero.ray_tracing.utils import count_segment_norm_angle, count_vec_mult
from res.utils.config import do_njit, cache, parallel
from res.utils.wrapper import clever_njit


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_curr_prev_att(cross_vec, curr_segment, fall_angle, border_arr):
    #print("start count_curr_prev_att: ", cross_vec, curr_segment, fall_angle)
    curr_point = count_curr_collision_cell(cross_vec, curr_segment)
    curr_att_x, curr_att_y = int(curr_point[0]), int(curr_point[1])
    angle = count_segment_norm_angle(curr_segment[0,0], curr_segment[0,1], curr_segment[1,0], curr_segment[1,1]) - np.pi*0.5

    if angle<0:
        angle+=2*np.pi
    #print("count angle: ", angle / np.pi)
    curr_f_num = 4.0*(angle/np.pi)
    if curr_f_num<0:
        curr_f_num+=8

    curr_f_num = int(curr_f_num)
    unfound = True
    #print("start find prev_att x,y")
    num = 0
    while unfound and num<10:
        num+=1
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

    if unfound:
        prev_att_x, prev_att_y = None, None


    #print("end count_curr_prev_att: ", curr_att_x, curr_att_y, prev_att_x, prev_att_y)
    return curr_att_x, curr_att_y, prev_att_x, prev_att_y, curr_f_num


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_curr_collision_cell(cross_vec, curr_segment):
    if (curr_segment[1]-curr_segment[0])[0]!=0:
        res_part=((cross_vec - curr_segment[0])[0])/((curr_segment[1]-curr_segment[0])[0])
    else:
        res_part=((cross_vec - curr_segment[0])[1])/((curr_segment[1]-curr_segment[0])[1])
    if (curr_segment[1]-curr_segment[0])[0]!=0 and (curr_segment[1]-curr_segment[0])[1]!=0:
        part = (cross_vec - curr_segment[0]) / (curr_segment[1] - curr_segment[0])
        if np.abs(part[0]-part[1])>10**(-5):
            print("Мы не на отрезке: ", cross_vec, curr_segment, part)

    if res_part<0.5 and curr_segment[1,1]-0.5!=0:
        return curr_segment[0]-0.5
    else:
        return curr_segment[1]-0.5


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
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
