from numba import njit
import numpy as np

from res.getero.reaction_consts.etching_consts import gamma_Cl_A, gamma_Cl_B, gamma_Cl_C, gamma_Cl_D
from res.getero.algorithm.utils import custom_choise


@njit()
def silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle):
    # Основное вещество (идёт активная реакция)
    if curr_type == 0:
        # радикал Хлора
        return clorine_etching(curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle)
    elif curr_type == 1:
        # ион Cl_plus
        pass
    elif curr_type == 2:
        # ион Ar_plus
        pass
    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, True, curr_angle


@njit()
def clorine_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle):
    p_sum = curr_counter[0]+curr_counter[1]+curr_counter[2]+curr_counter[3]
    p_A = gamma_Cl_A * curr_counter[0] / p_sum
    p_B = gamma_Cl_B * curr_counter[1] / p_sum
    p_C = gamma_Cl_C * curr_counter[2] / p_sum
    p_D = gamma_Cl_D * curr_counter[3] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D

    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])

    if curr_reaction == 4:
        is_react = False
        if is_on_horiz:
            curr_angle = np.pi - curr_angle
            if curr_angle < 0:
                curr_angle += 2.0 * np.pi
        else:
            curr_angle = 2.0 * np.pi - curr_angle
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, is_react, curr_angle

    is_react = True

    if curr_reaction == 0:
        curr_counter[0] -= 1
        curr_counter[1] += 1
    elif curr_reaction == 1:
        curr_counter[1] -= 1
        curr_counter[2] += 1
    elif curr_reaction == 2:
        curr_counter[2] -= 1
        curr_counter[3] += 1
    elif curr_reaction == 3:
        curr_counter[3] -= 1

    if curr_counter[0]+curr_counter[1]+curr_counter[2]+curr_counter[3] <= Si_num/2:
        curr_farr = 0
        curr_counter[0],curr_counter[1],curr_counter[2],curr_counter[3] = 0,0,0,0
    elif curr_counter[0]+curr_counter[1]+curr_counter[2]+curr_counter[3] >= 2 * Si_num:
        prev_farr = 1
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = Si_num, 0, 0, 0
        prev_counter[0], prev_counter[1], prev_counter[2], prev_counter[3] = Si_num, 0, 0, 0

    return curr_counter, prev_counter, curr_farr, prev_farr, is_react, curr_angle
