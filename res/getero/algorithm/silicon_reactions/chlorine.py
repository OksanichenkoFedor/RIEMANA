from res.getero.algorithm.silicon_reactions.cell_retraction import retract_cell
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.reaction_consts.sputtering_clorine import E_th_cl_sicl0_sp, E_th_cl_sicl1_sp, \
    E_th_cl_sicl2_sp, E_th_cl_sicl3_sp, \
    K_sp_cl_sicl0, K_sp_cl_sicl1, K_sp_cl_sicl2, K_sp_cl_sicl3
from res.getero.reaction_consts.ion_etching_clorine import E_th_Cl_ie, K_ie_cl_sicl, K_ie_cl_sicl2, K_ie_cl_sicl3, \
                                                           otn_const
from res.getero.reaction_consts.etching_clorine import gamma_Cl_A, gamma_Cl_B, gamma_Cl_C, gamma_Cl_D

from res.getero.algorithm.utils import custom_choise, straight_reflection, isotropic_reflection, count_falling_angle

from res.getero.reaction_consts.angular_dependences import ion_enh_etch_an_dep, sput_an_dep


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def clorine_etching(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0, 0]), int(point_vector[0, 1])
    p_sum = counter_arr[:, curr_x, curr_y].sum()
    p_A = gamma_Cl_A * counter_arr[0 ,curr_x, curr_y] / p_sum
    p_B = gamma_Cl_B * counter_arr[1 ,curr_x, curr_y] / p_sum
    p_C = gamma_Cl_C * counter_arr[2 ,curr_x, curr_y] / p_sum
    p_D = gamma_Cl_D * counter_arr[3 ,curr_x, curr_y] / p_sum
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
        counter_arr[0 ,curr_x, curr_y] -= 1
        counter_arr[1 ,curr_x, curr_y] += 1
    elif curr_reaction == 1:
        counter_arr[1 ,curr_x, curr_y] -= 1
        counter_arr[2 ,curr_x, curr_y] += 1
    elif curr_reaction == 2:
        counter_arr[2 ,curr_x, curr_y] -= 1
        counter_arr[3 ,curr_x, curr_y] += 1
    elif curr_reaction == 3:
        counter_arr[3 ,curr_x, curr_y] -= 1
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 8, 0, 0])

    # TODO разобраться с нормальным уничтожением ячейки

    if counter_arr[:, curr_x, curr_y].sum() <= Si_num/3:
        flags[2] = 1.0
        retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angles[0], False)

    return curr_type, curr_en, flags, redepo_params, angles[0]


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def clorine_ion_etching(curr_type, counter_arr, is_full_arr, point_vector, Si_num, angles, curr_en, R):
    flags = np.zeros(4)
    # flags = [is_react, is_redepo, is_delete, is_create]
    curr_x, curr_y = int(point_vector[0, 0]), int(point_vector[0, 1])
    c_sum = counter_arr[:, curr_x, curr_y].sum()

    p_sicl1_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl * counter_arr[1 ,curr_x, curr_y]
    p_sicl2_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl2 * \
                 counter_arr[2 ,curr_x, curr_y] * (counter_arr[0 ,curr_x, curr_y] / c_sum)
    p_sicl3_ie = otn_const * np.log(R+1) * max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_Cl_ie)) * K_ie_cl_sicl3 * \
                 counter_arr[3 ,curr_x, curr_y]

    curr_angle = count_falling_angle(angles[0], angles[1])

    p_sicl0_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl0_sp)) * K_sp_cl_sicl0 * counter_arr[0 ,curr_x, curr_y]
    p_sicl1_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl1_sp)) * K_sp_cl_sicl1 * counter_arr[1 ,curr_x, curr_y]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl2_sp)) * K_sp_cl_sicl2 * counter_arr[2 ,curr_x, curr_y]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_cl_sicl3_sp)) * K_sp_cl_sicl3 * counter_arr[3 ,curr_x, curr_y]

    # TODO распеределение по углам запилить и учесть шанс отражения

    p_sum = p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp + p_sicl1_ie + p_sicl2_ie + p_sicl3_ie

    if p_sum == 0:
        # никакой реакции не будет, пока что будем считать, что это отражение
        flags[0] = 0.0
        flags[1] = 0.0
        redepo_params = np.zeros((8))
        curr_type = 0  # ион хлора нейтрализуется
        new_angle = straight_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle

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
        flags[0] = 0.0
        flags[1] = 0.0
        redepo_params = np.zeros((8))
        curr_type = 0  # ион хлора нейтрализуется
        new_angle = straight_reflection(angles[0], angles[1])
        return curr_type, curr_en, flags, redepo_params, new_angle
    if curr_reaction == 0:
        # sp: Si_s -> Si_g
        curr_en = curr_en - E_th_cl_sicl0_sp
        curr_type = 0  # ион хлора нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[0, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 4, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - E_th_cl_sicl1_sp
        curr_type = 0
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[1, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 5, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - E_th_cl_sicl2_sp
        curr_type = 0  # ион хлора нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[2, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - E_th_cl_sicl3_sp
        curr_type = 0  # ион хлора нейтрализуется
        flags[0] = 0.0
        flags[1] = 1.0
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        new_angle = straight_reflection(angles[0], angles[1])
        counter_arr[3, curr_x, curr_y] -= 1
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 7, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 4:
        # i-etch: SiCl_s -> SiCl2_g
        flags[0] = 1.0
        flags[1] = 1.0
        counter_arr[1, curr_x, curr_y] -= 1
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 5:
        # i-etch: SiCl2_s + Si_s -> SiCl2_g + SiCl_s
        flags[0] = 1.0
        flags[1] = 1.0
        counter_arr[0, curr_x, curr_y] -= 1
        counter_arr[2, curr_x, curr_y] -= 1
        counter_arr[1, curr_x, curr_y] += 1
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6, 0, 0])
        # TODO угол отражённого иона
    elif curr_reaction == 6:
        # i-etch: SiCl3_s -> SiCl4_g
        flags[0] = 1.0
        flags[1] = 1.0
        counter_arr[3, curr_x, curr_y] -= 1
        redepo_angle = isotropic_reflection(angles[0], angles[1])
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 8, 0, 0])
        # TODO угол отражённого иона

    # TODO разобраться с нормальным уничтожением ячейки

    if counter_arr[:, curr_x, curr_y].sum() <= Si_num/3:
        flags[2] = 1.0
        retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angles[0], True)

    return curr_type, curr_en, flags, redepo_params, angles[0]
