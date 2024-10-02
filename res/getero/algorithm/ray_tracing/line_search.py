from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.algorithm.dynamic_profile import give_start
from res.getero.algorithm.ray_tracing.collision_functions import check_collision


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def simple_count_collision_point(border_layer_arr, ray_vec, curr_angle, start_segment):
    found = False
    cross_vec = np.zeros(2)
    dist2 = 0
    norm_angle = 0
    new_segment = np.ones((2,2))*(-1.0)
    x_start, y_start = give_start(border_layer_arr)
    x_end, y_end = border_layer_arr[x_start, y_start, 3:]
    unfound_end = True
    while unfound_end:
        if (border_layer_arr[x_end, y_end, 3] == -1) and (border_layer_arr[x_end, y_end, 4] == -1):
            unfound_end = False
        curr_segment = np.zeros((2,2))
        curr_segment[0, 0], curr_segment[0, 1] = x_start+0.5, y_start+0.5
        curr_segment[1, 0], curr_segment[1, 1] = x_end+0.5, y_end+0.5

        is_cross, curr_cross_vec, c_na  = check_collision(ray_vec, curr_angle, curr_segment)

        if is_cross:
            if found:
                c_d = np.sum((curr_cross_vec-ray_vec)*(curr_cross_vec-ray_vec))
                if dist2 > c_d and np.sum(np.abs(start_segment-curr_segment)):
                    dist2 = c_d
                    norm_angle = c_na
                    cross_vec = curr_cross_vec
                    new_segment = curr_segment
            else:
                if np.sum(np.abs(start_segment-curr_segment)):
                    found = True
                    cross_vec = curr_cross_vec
                    dist2 = np.sum((curr_cross_vec-ray_vec)*(curr_cross_vec-ray_vec))
                    norm_angle = c_na
                    new_segment = curr_segment

        x_start, y_start = x_end, y_end
        x_end, y_end = border_layer_arr[x_start, y_start, 3:]

    return found, cross_vec, norm_angle, new_segment









