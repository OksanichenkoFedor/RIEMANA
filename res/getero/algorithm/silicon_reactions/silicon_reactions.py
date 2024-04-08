from numba import njit
import numpy as np


from res.getero.reaction_consts.ion_etching_clorine import E_th_Cl_ie

from res.getero.algorithm.silicon_reactions.chlorine import clorine_etching, clorine_ion_etching

from res.getero.algorithm.silicon_reactions.argon import argon_sputtering


@njit()
def silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr, prev_farr,
                     Si_num, is_on_horiz, curr_angle, curr_en):
    # Основное вещество (идёт активная реакция)
    if curr_type == 0:
        # радикал Хлора
        if curr_en < E_th_Cl_ie:
            ans = clorine_etching(curr_type, curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)



            return ans
        else:
            ans = clorine_ion_etching(curr_type, curr_counter, prev_counter, curr_farr,
                                   prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)

            return ans
    elif curr_type == 1:
        # атом Ar
        ans = argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 2:
        # ион Cl_plus
        ans = clorine_ion_etching(curr_type, curr_counter, prev_counter, curr_farr,
                            prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)

        return ans
    elif curr_type == 3:
        # ион Ar_plus
        ans = argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                                  prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, True, curr_angle, curr_en, False, np.zeros((6))












