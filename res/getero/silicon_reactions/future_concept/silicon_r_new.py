from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.silicon_reactions.chlorine import clorine_etching#, clorine_ion_etching
#from res.getero.algorithm.silicon_reactions.argon import argon_sputtering
from res.getero.silicon_reactions.silicon_redepo import Si_redepo, SiCl_redepo, SiCl2_redepo
from res.getero.silicon_reactions.future_concept.ion_reaction import ion_etching

from res.getero.reaction_consts.sputtering_argon import sput_data_Ar_plus, E_th_ar_sicl3_sp
from res.getero.reaction_consts.sputtering_clorine import sput_data_Cl_plus, E_th_cl_sicl3_sp
from res.getero.reaction_consts.sputtering_cl2 import sput_data_Cl2_plus, E_th_cl2_sicl3_sp

from res.getero.algorithm.utils import straight_reflection


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr, prev_farr,
                     Si_num, is_on_horiz, curr_angle, curr_en):
    # Основное вещество (идёт активная реакция)
    if curr_type == 0:
        # радикал Хлора
        if curr_en < E_th_cl_sicl3_sp:
            ans = clorine_etching(curr_type, curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)



            return ans
        else:
            ans = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz,
                              curr_angle, curr_en, sput_data_Cl_plus)

            return ans
    elif curr_type == 1:
        # ион Cl2_plus
        curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle,
                          curr_en, sput_data_Cl2_plus)
        curr_type = 10
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params
    elif curr_type == 10:
        if curr_en > E_th_cl2_sicl3_sp:
            ans = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle,
                          curr_en, sput_data_Cl2_plus)
            return ans
    elif curr_type == 2:
        # ион Cl_plus
        curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle,
                          curr_en, sput_data_Cl_plus)
        curr_type = 0
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params
    elif curr_type == 3:
        # ион Ar_plus
        curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle,
                          curr_en, sput_data_Ar_plus)
        curr_type = 9
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
        is_react, curr_angle, curr_en, is_redepo, redepo_params
    elif curr_type == 9:
        if curr_en > E_th_ar_sicl3_sp:
            ans = ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz,
                              curr_angle, curr_en, sput_data_Ar_plus)
            return ans
    elif curr_type == 4:
        # Si попытка переосаждения
        print("Si r")
        ans = Si_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                                  prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 5:
        # SiCl попытка переосаждения
        print("SiCl")
        ans = SiCl_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                        prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 6:
        # SiCl2 попытка переосаждения
        print("SiCl2")
        ans = SiCl2_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                        prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 7:
        # SiCl3 попытка переосаждения
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
    elif curr_type == 8:
        # SiCl4 попытка переосаждения
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, False, curr_angle, curr_en, False, np.zeros((6))












