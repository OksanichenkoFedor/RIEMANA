from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.reaction_consts.sputtering_argon import E_th_ar_sicl0_sp, E_th_ar_sicl1_sp, \
                                                          E_th_ar_sicl2_sp, E_th_ar_sicl3_sp,\
                                                          K_sp_ar_sicl0, K_sp_ar_sicl1, K_sp_ar_sicl2, K_sp_ar_sicl3

from res.getero.algorithm.utils import custom_choise, straight_reflection, isotropic_reflection, count_falling_angle

from res.getero.reaction_consts.angular_dependences import sput_an_dep

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, normal_angle, start_angle, curr_en):
    c_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]

    p_sicl0_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl0_sp)) * K_sp_ar_sicl0 * curr_counter[0]
    p_sicl1_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl1_sp)) * K_sp_ar_sicl1 * curr_counter[1]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl2_sp)) * K_sp_ar_sicl2 * curr_counter[2]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl3_sp)) * K_sp_ar_sicl3 * curr_counter[3]

    curr_angle = count_falling_angle(start_angle, normal_angle)

    p_sum = p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp

    if p_sum==0:
        #print("fffffffff")
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((6))
        curr_type = 9  # ион аргона нейтрализуется
        start_angle = isotropic_reflection(start_angle, normal_angle)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, start_angle, curr_en, is_redepo, redepo_params

    p_sicl0_sp = p_sicl0_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl1_sp = p_sicl1_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl2_sp = p_sicl2_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl3_sp = p_sicl3_sp * sput_an_dep(curr_angle) / p_sum

    p_refl = 1.0 - (p_sicl0_sp+p_sicl1_sp+p_sicl2_sp+p_sicl3_sp)

    curr_reaction = custom_choise([p_sicl0_sp, p_sicl1_sp, p_sicl2_sp, p_sicl3_sp, p_refl])


    if curr_reaction==4:
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((8))
        curr_type = 9 # ион аргона нейтрализуется
        start_angle = straight_reflection(start_angle, normal_angle)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, start_angle, curr_en, is_redepo, redepo_params
    if curr_reaction==0:
        # sp: Si_s -> Si_g
        curr_en = curr_en-E_th_ar_sicl0_sp
        curr_type = 9 # ион аргона нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[0] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 4, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - E_th_ar_sicl1_sp
        curr_type = 9  # ион аргона нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[1] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 5, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - E_th_ar_sicl2_sp
        curr_type = 9  # ион аргона нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[2] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - E_th_ar_sicl3_sp
        curr_type = 9  # ион аргона нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[3] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 7, 0, 0])
        # TODO угол отражённого иона

    # TODO разобраться с нормальным уничтожением ячейки

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] <= 0:
        curr_farr = 0
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = 0, 0, 0, 0

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
           is_react, start_angle, curr_en, is_redepo, redepo_params