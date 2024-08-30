from numba import njit
import numpy as np

from res.getero.reaction_consts.sputtering_clorine import E_th_cl_sicl0_sp, E_th_cl_sicl1_sp, \
    E_th_cl_sicl2_sp, E_th_cl_sicl3_sp, \
    K_sp_cl_sicl0, K_sp_cl_sicl1, K_sp_cl_sicl2, K_sp_cl_sicl3
from res.getero.reaction_consts.ion_etching_clorine import E_th_Cl_ie, K_ie_cl_sicl, K_ie_cl_sicl2, K_ie_cl_sicl3, \
                                                           otn_const
from res.getero.reaction_consts.etching_clorine import gamma_Cl_A, gamma_Cl_B, gamma_Cl_C, gamma_Cl_D

from res.getero.algorithm.utils import custom_choise, straight_reflection, isotropic_reflection

from res.getero.reaction_consts.angular_dependences import ion_enh_etch_an_dep, sput_an_dep


@njit()
def clorine_etching(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, normal_angle, start_angle, curr_en):
    p_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]
    p_A = gamma_Cl_A * curr_counter[0] / p_sum
    p_B = gamma_Cl_B * curr_counter[1] / p_sum
    p_C = gamma_Cl_C * curr_counter[2] / p_sum
    p_D = gamma_Cl_D * curr_counter[3] / p_sum
    p_refl = 1.0 - p_A - p_B - p_C - p_D

    curr_reaction = custom_choise([p_A, p_B, p_C, p_D, p_refl])

    is_redepo = False
    redepo_params = np.zeros((8))

    if curr_reaction == 4:
        is_react = False

        start_angle = isotropic_reflection(start_angle, normal_angle)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, start_angle, curr_en, is_redepo, redepo_params

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
        is_redepo = True
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 8, 0, 0])

    # TODO разобраться с нормальным уничтожением ячейки

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] <= 0:
        curr_farr = 0
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = 0, 0, 0, 0

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
           is_react, start_angle, curr_en, is_redepo, redepo_params


@njit()
def clorine_ion_etching(curr_type, curr_counter, prev_counter, curr_farr,
                        prev_farr, Si_num, normal_angle, start_angle, curr_en, R):
    c_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]

    p_sicl1_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl * curr_counter[
        1]
    p_sicl2_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl2 * \
                 curr_counter[2] * (curr_counter[0] / c_sum)
    p_sicl3_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl3 * \
                 curr_counter[3]

    curr_angle = np.abs(normal_angle - (np.pi + start_angle))

    p_sicl0_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl0_sp)) * K_sp_cl_sicl0 * curr_counter[0]
    p_sicl1_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl1_sp)) * K_sp_cl_sicl1 * curr_counter[1]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl2_sp)) * K_sp_cl_sicl2 * curr_counter[2]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl3_sp)) * K_sp_cl_sicl3 * curr_counter[3]

    # TODO распеределение по углам запилить и учесть шанс отражения

    p_sum = p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp + p_sicl1_ie + p_sicl2_ie + p_sicl3_ie

    if p_sum == 0:
        # никакой реакции не будет, пока что будем считать, что это отражение
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((8))
        curr_type = 0  # ион хлора нейтрализуется
        start_angle = straight_reflection(start_angle, normal_angle)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, start_angle, curr_en, is_redepo, redepo_params
    p_sicl1_ie = p_sicl1_ie * ion_enh_etch_an_dep(curr_angle) / p_sum
    p_sicl2_ie = p_sicl2_ie * ion_enh_etch_an_dep(curr_angle) / p_sum
    p_sicl3_ie = p_sicl3_ie * ion_enh_etch_an_dep(curr_angle) / p_sum

    p_sicl0_sp = p_sicl0_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl1_sp = p_sicl1_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl2_sp = p_sicl2_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl3_sp = p_sicl3_sp * sput_an_dep(curr_angle) / p_sum

    p_refl = 1.0 - (p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp) - (p_sicl1_ie + p_sicl2_ie + p_sicl3_ie)

    curr_reaction = custom_choise([p_sicl0_sp, p_sicl1_sp, p_sicl2_sp, p_sicl3_sp,
                                   p_sicl1_ie, p_sicl2_ie, p_sicl3_ie, p_refl])

    if curr_reaction == 7:
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((8))
        curr_type = 0  # ион хлора нейтрализуется
        start_angle = straight_reflection(start_angle, normal_angle)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, start_angle, curr_en, is_redepo, redepo_params
    if curr_reaction == 0:
        # sp: Si_s -> Si_g
        curr_en = curr_en - E_th_cl_sicl0_sp
        curr_type = 0  # ион хлора нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[0] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 4, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - E_th_cl_sicl1_sp
        curr_type = 0
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[1] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 5, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - E_th_cl_sicl2_sp
        curr_type = 0  # ион хлора нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[2] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - E_th_cl_sicl3_sp
        curr_type = 0  # ион хлора нейтрализуется
        is_react = False
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        start_angle = straight_reflection(start_angle, normal_angle)
        curr_counter[3] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 7, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 4:
        # i-etch: SiCl_s -> SiCl2_g
        is_react = True
        curr_counter[1] -= 1
        is_redepo = True
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 5:
        # i-etch: SiCl2_s + Si_s -> SiCl2_g + SiCl_s
        is_react = True
        curr_counter[0] -= 1
        curr_counter[2] -= 1
        curr_counter[1] += 1
        is_redepo = True
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 6:
        # i-etch: SiCl3_s -> SiCl4_g
        is_react = True
        curr_counter[3] -= 1
        is_redepo = True
        redepo_angle = isotropic_reflection(start_angle, normal_angle)
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 8, 0, 0])
        # TODO угол отражённого иона

    # TODO разобраться с нормальным уничтожением ячейки

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] <= 0:
        curr_farr = 0
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = 0, 0, 0, 0

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
           is_react, start_angle, curr_en, is_redepo, redepo_params