from numba import njit
import numpy as np

from res.getero.algorithm.utils import custom_choise, straight_reflection

from res.getero.reaction_consts.redepo_silicon import gamma_Si_redepo, gamma_Si_SiCl_redepo, gamma_SiCl2_SiCl_redepo, \
    gamma_SiCl_SiCl_redepo, gamma_SiCl3_SiCl_redepo, gamma_Si_SiCl2_redepo, \
    gamma_SiCl_SiCl2_redepo, gamma_SiCl2_SiCl2_redepo, gamma_SiCl3_SiCl2_redepo

@njit()
def Si_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, is_on_horiz, curr_angle, curr_en):
    p_Si_redepo = gamma_Si_redepo
    p_refl = 1.0 - p_Si_redepo
    curr_reaction = custom_choise([p_Si_redepo, p_refl])

    is_redepo = False
    redepo_params = np.zeros((6))

    if curr_reaction == 1:
        is_react = False
        # TODO нормальное отражение прописать
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params
    print("Si react")
    is_react = True
    if curr_reaction == 0:
        curr_counter[0] += 1

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] >= 2 * Si_num:
        prev_farr = 1
        prev_counter[0], prev_counter[1], prev_counter[2], prev_counter[3] = curr_counter[0] / 2, curr_counter[1] / 2, \
                                                                             curr_counter[2] / 2, curr_counter[3] / 2
        curr_counter[0] = curr_counter[0] - prev_counter[0]
        curr_counter[1] = curr_counter[1] - prev_counter[1]
        curr_counter[2] = curr_counter[2] - prev_counter[2]
        curr_counter[3] = curr_counter[3] - prev_counter[3]

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params

@njit()
def SiCl_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, is_on_horiz, curr_angle, curr_en):
    p_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]
    p_A = gamma_Si_SiCl2_redepo * curr_counter[0] / p_sum
    p_B = gamma_SiCl_SiCl2_redepo * curr_counter[1] / p_sum
    p_C = gamma_SiCl2_SiCl2_redepo * curr_counter[2] / p_sum
    p_D = gamma_SiCl3_SiCl2_redepo * curr_counter[3] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D

    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])

    is_redepo = False
    redepo_params = np.zeros((6))

    if curr_reaction == 4:
        is_react = False
        # TODO нормальное отражение прописать
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params

    is_react = True
    if curr_reaction == 0:
        curr_counter[1] += 1
    elif curr_reaction == 1:
        curr_counter[1] += 1
    elif curr_reaction == 2:
        curr_counter[1] += 1
    elif curr_reaction == 3:
        curr_counter[1] += 1

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] >= 2 * Si_num:
        prev_farr = 1
        prev_counter[0], prev_counter[1], prev_counter[2], prev_counter[3] = curr_counter[0] / 2, curr_counter[1] / 2, \
                                                                             curr_counter[2] / 2, curr_counter[3] / 2
        curr_counter[0] = curr_counter[0] - prev_counter[0]
        curr_counter[1] = curr_counter[1] - prev_counter[1]
        curr_counter[2] = curr_counter[2] - prev_counter[2]
        curr_counter[3] = curr_counter[3] - prev_counter[3]

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params


@njit()
def SiCl2_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, is_on_horiz, curr_angle, curr_en):
    p_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]
    p_A = gamma_Si_SiCl_redepo * curr_counter[0] / p_sum
    p_B = gamma_SiCl_SiCl_redepo * curr_counter[1] / p_sum
    p_C = gamma_SiCl2_SiCl_redepo * curr_counter[2] / p_sum
    p_D = gamma_SiCl3_SiCl_redepo * curr_counter[3] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D

    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])

    is_redepo = False
    redepo_params = np.zeros((6))

    if curr_reaction == 4:
        is_react = False
        # TODO нормальное отражение прописать
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params

    is_react = True
    if curr_reaction == 0:
        curr_counter[2] += 1
    elif curr_reaction == 1:
        curr_counter[2] += 1
    elif curr_reaction == 2:
        curr_counter[2] += 1
    elif curr_reaction == 3:
        curr_counter[2] += 1

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] >= 2 * Si_num:
        prev_farr = 1
        prev_counter[0], prev_counter[1], prev_counter[2], prev_counter[3] = curr_counter[0]/2, curr_counter[1]/2, \
                                                                             curr_counter[2]/2, curr_counter[3]/2
        curr_counter[0] = curr_counter[0] - prev_counter[0]
        curr_counter[1] = curr_counter[1] - prev_counter[1]
        curr_counter[2] = curr_counter[2] - prev_counter[2]
        curr_counter[3] = curr_counter[3] - prev_counter[3]

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params
