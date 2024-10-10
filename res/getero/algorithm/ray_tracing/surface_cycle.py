import numpy as np

from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def surface_cycle(counter_arr,  is_full_arr, curr_angle, normal_angle, curr_att_x, curr_att_y, prev_att_x, prev_att_y, curr_type, Si_num, curr_en, R):
    angles = np.zeros(2)
    angles[0], angles[1] = curr_angle, normal_angle

    point_vector = np.zeros((2, 2))
    point_vector[0, 0], point_vector[0, 1] = curr_att_x, curr_att_y
    point_vector[1, 0], point_vector[1, 1] = prev_att_x, prev_att_y

    if counter_arr[:, curr_att_x, curr_att_y].sum() == 0.0:
        print("---")
        print("Пустая не пустая!!!")
        print(curr_att_x, curr_att_y)
        print("---")

    new_type, new_en, flags, redepo_params, new_angle = silicon_reaction(curr_type, counter_arr,
                                                                         is_full_arr, point_vector,
                                                                         Si_num, angles, curr_en, R)
    return new_type, new_en, flags, redepo_params, new_angle