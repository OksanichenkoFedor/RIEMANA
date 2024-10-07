from res.getero.algorithm.silicon_reactions.cell_retraction import retract_cell
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.reaction_consts.sputtering_argon import E_th_ar_sicl0_sp, E_th_ar_sicl1_sp, \
                                                          E_th_ar_sicl2_sp, E_th_ar_sicl3_sp,\
                                                          K_sp_ar_sicl0, K_sp_ar_sicl1, K_sp_ar_sicl2, K_sp_ar_sicl3

from res.getero.algorithm.utils import custom_choise, straight_reflection, isotropic_reflection, count_falling_angle

from res.getero.reaction_consts.angular_dependences import sput_an_dep

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def argon_sputtering(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    #print("ffff")
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0,0]), int(point_vector[0,1])
    c_sum = counter_arr[:, curr_x, curr_y].sum()

    p_sicl0_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl0_sp)) * K_sp_ar_sicl0 * counter_arr[0 ,curr_x, curr_y]
    p_sicl1_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl1_sp)) * K_sp_ar_sicl1 * counter_arr[1 ,curr_x, curr_y]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl2_sp)) * K_sp_ar_sicl2 * counter_arr[2 ,curr_x, curr_y]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl3_sp)) * K_sp_ar_sicl3 * counter_arr[3 ,curr_x, curr_y]

    curr_angle = count_falling_angle(angles[0], angles[1])

    p_sum = p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp

    if p_sum==0:
        #print("fffffffff")
        flags[0]=0.0
        flags[1]=0.0
        redepo_params = np.zeros((6))
        curr_type = 9  # ион аргона нейтрализуется
        new_angle = isotropic_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle

    p_sicl0_sp = p_sicl0_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl1_sp = p_sicl1_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl2_sp = p_sicl2_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl3_sp = p_sicl3_sp * sput_an_dep(curr_angle) / p_sum

    p_refl = 1.0 - (p_sicl0_sp+p_sicl1_sp+p_sicl2_sp+p_sicl3_sp)

    curr_reaction = custom_choise([p_sicl0_sp, p_sicl1_sp, p_sicl2_sp, p_sicl3_sp, p_refl])


    if curr_reaction==4:
        flags[0] = 0.0
        flags[1] = 0.0
        redepo_params = np.zeros((8))
        curr_type = 9 # ион аргона нейтрализуется
        new_angle = straight_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle
    if curr_reaction==0:
        # sp: Si_s -> Si_g
        curr_en = curr_en-E_th_ar_sicl0_sp
        curr_type = 9 # ион аргона нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[0, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 4, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - E_th_ar_sicl1_sp
        curr_type = 9  # ион аргона нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[1, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 5, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - E_th_ar_sicl2_sp
        curr_type = 9  # ион аргона нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[2, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction==3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - E_th_ar_sicl3_sp
        curr_type = 9  # ион аргона нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[3, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 7, 0, 0])
        # TODO угол отражённого иона

    # TODO разобраться с нормальным уничтожением ячейки

    if counter_arr[:, curr_x, curr_y].sum() <= 0:#Si_num/5:
        flags[2] = 1.0
        retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angles[0], False)

    return curr_type, curr_en, flags, redepo_params, new_angle