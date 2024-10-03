from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

from res.getero.reaction_consts.angular_dependences import ion_enh_etch_an_dep, sput_an_dep

from res.getero.algorithm.utils import custom_choise, straight_reflection, isotropic_reflection


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def ion_etching(curr_type, curr_counter, prev_counter, curr_farr, prev_farr, Si_num, is_on_horiz, curr_angle, curr_en,
                sput_data):
    c_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]

    # p_sicl0_ie = otn_param * np.log(1 + R_ion) * max(0.0, np.sqrt(curr_en) - np.sqrt(ion_enh_data[0][0])) * \
    #             ion_enh_data[1][0] * curr_counter[1]
    # p_sicl1_ie = otn_param * np.log(1 + R_ion) * max(0.0, np.sqrt(curr_en) - np.sqrt(ion_enh_data[0][1])) * \
    #             ion_enh_data[1][1] * curr_counter[2] * (curr_counter[0] / c_sum)
    # p_sicl2_ie = otn_param * np.log(1 + R_ion) * max(0.0, np.sqrt(curr_en) - np.sqrt(ion_enh_data[0][1])) * \
    #             ion_enh_data[1][1] * curr_counter[3]

    p_sicl0_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(sput_data[0][0])) * sput_data[1][0] * curr_counter[0]
    p_sicl1_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(sput_data[0][1])) * sput_data[1][1] * curr_counter[1]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(sput_data[0][2])) * sput_data[1][2] * curr_counter[2]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(sput_data[0][3])) * sput_data[1][3] * curr_counter[3]

    p_sum = p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp  # + p_sicl0_ie + p_sicl1_ie + p_sicl2_ie

    if p_sum == 0:
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((8))
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params

    # p_sicl0_ie = p_sicl0_ie * ion_enh_etch_an_dep(curr_angle) / p_sum
    # p_sicl1_ie = p_sicl1_ie * ion_enh_etch_an_dep(curr_angle) / p_sum
    # p_sicl2_ie = p_sicl2_ie * ion_enh_etch_an_dep(curr_angle) / p_sum

    p_sicl0_sp = p_sicl0_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl1_sp = p_sicl1_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl2_sp = p_sicl2_sp * sput_an_dep(curr_angle) / p_sum
    p_sicl3_sp = p_sicl3_sp * sput_an_dep(curr_angle) / p_sum

    # p_refl = 1.0 - (p_sicl0_ie+p_sicl1_ie+p_sicl2_ie) - (p_sicl0_sp+p_sicl1_sp+p_sicl2_sp+p_sicl3_sp)
    p_refl = 1.0 - (p_sicl0_sp + p_sicl1_sp + p_sicl2_sp + p_sicl3_sp)

    curr_reaction = custom_choise([p_sicl0_sp, p_sicl1_sp, p_sicl2_sp, p_sicl3_sp, p_refl])
    #                               p_sicl0_ie, p_sicl1_ie, p_sicl2_ie, p_refl])

    if curr_reaction == 4:
        # Отражение
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((8))
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params
    if curr_reaction == 0:
        # sp: Si_s -> Si_g
        curr_en = curr_en - sput_data[0][0]
        curr_counter[0] -= 1
        redepo_type = 4
    elif curr_reaction == 1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - sput_data[0][1]
        curr_counter[1] -= 1
        redepo_type = 5
    elif curr_reaction == 2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - sput_data[0][2]
        curr_counter[2] -= 1
        redepo_type = 6
    elif curr_reaction == 3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - sput_data[0][3]
        curr_counter[3] -= 1
        redepo_type = 7

    is_react = False
    redepo_angle = isotropic_reflection(curr_angle, is_on_horiz)
    curr_angle = straight_reflection(curr_angle, is_on_horiz)

    is_redepo = True
    redepo_params = np.array([0, 0, 0, 0, redepo_angle, redepo_type, 0, 0])

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] <= 0:
        curr_farr = 0
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = 0, 0, 0, 0

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
           is_react, curr_angle, curr_en, is_redepo, redepo_params
