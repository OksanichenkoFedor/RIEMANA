from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np


from res.getero.reaction_consts.ion_etching_clorine import E_th_Cl_ie

from res.getero.algorithm.silicon_reactions.chlorine import clorine_etching, clorine_ion_etching
from res.getero.algorithm.silicon_reactions.argon import argon_sputtering
from res.getero.algorithm.silicon_reactions.silicon_redepo import Si_redepo, SiCl_redepo, SiCl2_redepo

from res.getero.algorithm.utils import straight_reflection, isotropic_reflection


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def silicon_reaction(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    # point_vector = [[curr_att_x, curr_att_y],
    #                  [prev_att_x, prev_att_y]]
    # angles = [normal_angle, start_angle]
    # Основное вещество (идёт активная реакция)
    if curr_type == 0:
        # радикал Хлора
        if curr_en < E_th_Cl_ie:
            ans = clorine_etching(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
            return ans
        else:
            ans = clorine_ion_etching(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
            return ans
    elif curr_type == 9:
        # атом Ar
        ans = argon_sputtering(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
        return ans
    elif curr_type == 2:
        # ион Cl_plus
        ans = clorine_ion_etching(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)

        return ans
    elif curr_type == 3:
        # ион Ar_plus
        ans = argon_sputtering(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
        return ans
    elif curr_type == 4:
        # Si попытка переосаждения
        ans = Si_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
        return ans
    elif curr_type == 5:
        # SiCl попытка переосаждения
        ans = SiCl_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
        return ans
    elif curr_type == 6:
        # SiCl2 попытка переосаждения
        ans = SiCl2_redepo(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R)
        return ans
    elif curr_type == 7:
        # SiCl3 попытка переосаждения
        start_angle = isotropic_reflection(angles[0], angles[1])
    elif curr_type == 8:
        # SiCl4 попытка переосаждения
        start_angle = isotropic_reflection(angles[0], angles[1])
    elif curr_type == 1:
        print("Cl2_plus")

    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    redepo_params = np.zeros((8))
    return curr_type, curr_en, flags, redepo_params, angles[0]