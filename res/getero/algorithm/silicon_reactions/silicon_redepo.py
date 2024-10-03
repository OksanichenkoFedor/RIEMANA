from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.algorithm.utils import custom_choise, isotropic_reflection

from res.getero.reaction_consts.redepo_silicon import gamma_Si_redepo, gamma_Si_SiCl_redepo, gamma_SiCl2_SiCl_redepo, \
    gamma_SiCl_SiCl_redepo, gamma_SiCl3_SiCl_redepo, gamma_Si_SiCl2_redepo, \
    gamma_SiCl_SiCl2_redepo, gamma_SiCl2_SiCl2_redepo, gamma_SiCl3_SiCl2_redepo

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def Si_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0, 0]), int(point_vector[0, 1])
    prev_x, prev_y = int(point_vector[1, 0]), int(point_vector[1, 1])
    p_Si_redepo = gamma_Si_redepo
    p_refl = 1.0 - p_Si_redepo
    curr_reaction = custom_choise([p_Si_redepo, p_refl])

    flags[1] = 0.0
    redepo_params = np.zeros((8))

    if curr_reaction == 1:
        flags[0] = 0.0
        new_angle = isotropic_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle
    flags[0] = 1.0
    if curr_reaction == 0:
        counter_arr[0 ,curr_x, curr_y] += 1

    if counter_arr[:, curr_x, curr_y].sum() >= 2 * Si_num:
        flags[3] = 1.0
        is_full_arr[prev_x, prev_y] = 1.0
        for i in range(4):
            counter_arr[i, prev_x, prev_y] = int(counter_arr[i, curr_x, curr_y]) / 2
        counter_arr[:, curr_x, curr_y] = counter_arr[:, curr_x, curr_y] - counter_arr[:, prev_x, prev_y]

    return curr_type, curr_en, flags, redepo_params, angles[0]

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def SiCl_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0, 0]), int(point_vector[0, 1])
    prev_x, prev_y = int(point_vector[1, 0]), int(point_vector[1, 1])
    p_sum = counter_arr[:, curr_x, curr_y].sum()
    p_A = gamma_Si_SiCl2_redepo * counter_arr[0 ,curr_x, curr_y] / p_sum
    p_B = gamma_SiCl_SiCl2_redepo * counter_arr[1 ,curr_x, curr_y] / p_sum
    p_C = gamma_SiCl2_SiCl2_redepo * counter_arr[2 ,curr_x, curr_y] / p_sum
    p_D = gamma_SiCl3_SiCl2_redepo * counter_arr[3 ,curr_x, curr_y] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D

    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])

    flags[1] = 0.0
    redepo_params = np.zeros((8))

    if curr_reaction == 4:
        flags[0] = 0.0
        new_angle = isotropic_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle

    flags[0] = 1.0
    if curr_reaction == 0:
        counter_arr[1 ,curr_x, curr_y] += 1
    elif curr_reaction == 1:
        counter_arr[1 ,curr_x, curr_y] += 1
    elif curr_reaction == 2:
        counter_arr[1 ,curr_x, curr_y] += 1
    elif curr_reaction == 3:
        counter_arr[1 ,curr_x, curr_y] += 1

    if counter_arr[:, curr_x, curr_y].sum() >= 2 * Si_num:
        flags[3] = 1.0
        is_full_arr[prev_x, prev_y] = 1.0
        for i in range(4):
            counter_arr[i, prev_x, prev_y] = int(counter_arr[i, curr_x, curr_y])/2
        counter_arr[:, curr_x, curr_y] = counter_arr[:, curr_x, curr_y] - counter_arr[:, prev_x, prev_y]

    return curr_type, curr_en, flags, redepo_params, angles[0]


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def SiCl2_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0, 0]), int(point_vector[0, 1])
    prev_x, prev_y = int(point_vector[1, 0]), int(point_vector[1, 1])
    p_sum = counter_arr[:, curr_x, curr_y].sum()
    p_A = gamma_Si_SiCl_redepo * counter_arr[0 ,curr_x, curr_y] / p_sum
    p_B = gamma_SiCl_SiCl_redepo * counter_arr[1 ,curr_x, curr_y] / p_sum
    p_C = gamma_SiCl2_SiCl_redepo * counter_arr[2 ,curr_x, curr_y] / p_sum
    p_D = gamma_SiCl3_SiCl_redepo * counter_arr[3 ,curr_x, curr_y] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D
    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])
    flags[1] = 0.0
    redepo_params = np.zeros((8))

    if curr_reaction == 4:
        flags[0] = 0.0
        new_angle = isotropic_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle

    flags[0] = 1.0
    if curr_reaction == 0:
        counter_arr[2 ,curr_x, curr_y] += 1
    elif curr_reaction == 1:
        counter_arr[2 ,curr_x, curr_y] += 1
    elif curr_reaction == 2:
        counter_arr[2 ,curr_x, curr_y] += 1
    elif curr_reaction == 3:
        counter_arr[2 ,curr_x, curr_y] += 1

    if counter_arr[:, curr_x, curr_y].sum() >= 2 * Si_num:
        flags[3] = 1.0
        is_full_arr[prev_x, prev_y] = 1.0
        for i in range(4):
            counter_arr[i, prev_x, prev_y] = int(counter_arr[i, curr_x, curr_y]) / 2
        counter_arr[:, curr_x, curr_y] = counter_arr[:, curr_x, curr_y] - counter_arr[:, prev_x, prev_y]

    return curr_type, curr_en, flags, redepo_params, angles[0]