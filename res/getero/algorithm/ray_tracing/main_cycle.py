import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numba as nb

from res.getero.algorithm.utils import straight_reflection
from res.getero.algorithm.ray_tracing.ray_tracing import simple_count_collision_point

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                         returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                         params, Si_num, xsize, ysize, R, test, do_half, max_value):
    curr_x = params[0]
    curr_y = params[1]
    start_segm_x, start_segm_y = -1, -1
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    unfound = True
    not_max_value = True
    if test:
        pass
        arr_x.append(curr_x - 0.5)
        arr_y.append(curr_y - 0.5)
    while unfound and not_max_value:
        is_collide, x_collide, y_collide, norm_angle, start_segm_x, start_segm_y = simple_count_collision_point(border_layer_arr, curr_x, curr_y, curr_angle, start_segm_x, start_segm_y)
        if is_collide:
            if test:
                pass
                arr_x.append(x_collide - 0.5)
                arr_y.append(y_collide - 0.5)
            curr_att_x, curr_att_y = int(x_collide), int(y_collide)
            #print(x_collide, y_collide, curr_angle/np.pi, norm_angle/np.pi, is_full_arr[curr_att_x, curr_att_y])
            if is_full_arr[curr_att_x, curr_att_y] == 1.0:
                #
                curr_angle = straight_reflection(curr_angle, norm_angle)
                #print(curr_angle/np.pi)
            elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
                # Маска
                curr_angle = straight_reflection(curr_angle, norm_angle)
            else:
                #print("Мы ударились о пустоту!")
                curr_angle = straight_reflection(curr_angle, norm_angle)
            curr_x, curr_y = x_collide, y_collide
        else:
            unfound = False
            if test:
                pass
                arr_x.append(curr_x - 0.5 + np.sin(curr_angle)*5)
                arr_y.append(curr_y - 0.5 + np.cos(curr_angle)*5)




@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_particles(counter_arr, is_full_arr, border_layer_arr, params_arr, Si_num, xsize, ysize, R, test, do_half,
                      max_value=-1.0):
    if test:
        arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                       nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    else:
        arr_x, arr_y, rarr_x, rarr_y = None, None, None, None

    returned_particles = np.zeros(11)
    for i in range(len(params_arr)):
        curr_params_arr = params_arr[i]
        process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                             returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                             curr_params_arr, Si_num, xsize, ysize, R, test, do_half, max_value)
    return returned_particles, arr_x, arr_y, rarr_x, rarr_y