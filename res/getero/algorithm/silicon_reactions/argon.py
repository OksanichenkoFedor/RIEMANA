from numba import njit
import numpy as np

from res.getero.reaction_consts.sputtering_argon import E_th_ar_si_sp, E_th_ar_sicl_sp, \
                                                          E_th_ar_sicl2_sp, E_th_ar_sicl3_sp,\
                                                          K_sp_ar_si, K_sp_ar_sicl, K_sp_ar_sicl2, K_sp_ar_sicl3

from res.getero.algorithm.utils import custom_choise, straight_reflection

@njit()
def argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                    prev_farr, Si_num, is_on_horiz, curr_angle, curr_en):
    c_sum = curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3]

    p_si_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_si_sp)) * K_sp_ar_si * curr_counter[0]
    p_sicl_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl_sp)) * K_sp_ar_sicl * curr_counter[1]
    p_sicl2_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl2_sp)) * K_sp_ar_sicl2 * curr_counter[2]
    p_sicl3_sp = max(0.0, np.sqrt(curr_en) - np.sqrt(E_th_ar_sicl3_sp)) * K_sp_ar_sicl3 * curr_counter[3]

    # TODO распеределение по углам запилить и учесть шанс отражения

    p_sum = p_si_sp + p_sicl_sp + p_sicl2_sp + p_sicl3_sp

    if p_sum==0:
        # никакой реакции не будет, пока что будем считать, что это отражение
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((6))
        curr_type = 1  # ион аргона нейтрализуется
        curr_en = 0.9 * curr_en  # энергия теряется #TODO допилить нормальные потери энергии
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        # TODO добавить рассеяние при отражении
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params

    p_si_sp, p_sicl_sp, p_sicl2_sp, p_sicl3_sp = 1.0 * p_si_sp / p_sum, 1.0 * p_sicl_sp / p_sum, \
                                                 1.0 * p_sicl2_sp / p_sum, 1.0 * p_sicl3_sp / p_sum

    p_refl = 0.0

    curr_reaction = custom_choise([p_si_sp, p_sicl_sp, p_sicl2_sp, p_sicl3_sp, p_refl])


    if curr_reaction==4:
        is_react = False
        is_redepo = False
        redepo_params = np.zeros((6))
        curr_type = 1 # ион аргона нейтрализуется
        curr_en = 0.9*curr_en # энергия теряется #TODO допилить нормальные потери энергии
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        #TODO добавить рассеяние при отражении
        return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
               is_react, curr_angle, curr_en, is_redepo, redepo_params
    if curr_reaction==0:
        # sp: Si_s -> Si_g
        curr_en = curr_en-E_th_ar_si_sp #TODO узнать как на самом деле менятся энергии после участия в процессе распыления
        curr_type = 1 # ион аргона нейтрализуется TODO уточнить, что происходит и ионами после участия в процессе распыления
        is_react = False
        redepo_angle = straight_reflection(curr_angle, is_on_horiz)
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        # TODO добавить рассеяние при отражении
        curr_counter[0] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 4])
        # TODO угол выбитых частиц
    elif curr_reaction==1:
        # sp: SiCl_s -> SiCl_g
        curr_en = curr_en - E_th_ar_sicl_sp #TODO узнать как на самом деле менятся энергии после участия в процессе распыления
        curr_type = 1  # ион аргона нейтрализуется TODO уточнить, что происходит и ионами после участия в процессе распыления
        is_react = False
        redepo_angle = straight_reflection(curr_angle, is_on_horiz)
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        # TODO добавить рассеяние при отражении
        curr_counter[1] -= 1
        is_redepo = True

        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 5])
        # TODO угол выбитых частиц
    elif curr_reaction==2:
        # sp: SiCl2_s -> SiCl2_g
        curr_en = curr_en - E_th_ar_sicl2_sp #TODO узнать как на самом деле менятся энергии после участия в процессе распыления
        curr_type = 1  # ион аргона нейтрализуется TODO уточнить, что происходит и ионами после участия в процессе распыления
        is_react = False
        redepo_angle = straight_reflection(curr_angle, is_on_horiz)
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        # TODO добавить рассеяние при отражении
        curr_counter[2] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 6])
        # TODO угол выбитых частиц
    elif curr_reaction==3:
        # sp: SiCl3_s -> SiCl3_g
        curr_en = curr_en - E_th_ar_sicl3_sp #TODO узнать как на самом деле менятся энергии после участия в процессе распыления
        curr_type = 0  # ион аргона нейтрализуется TODO уточнить, что происходит и ионами после участия в процессе распыления
        is_react = False
        redepo_angle = straight_reflection(curr_angle, is_on_horiz)
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
        # TODO добавить рассеяние при отражении
        curr_counter[3] -= 1
        is_redepo = True
        redepo_params = np.array([0, 0, 0, 0, redepo_angle, 7])
        # TODO угол выбитых частиц

    # TODO разобраться с нормальным уничтожением ячейки

    if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] <= 0:
        curr_farr = 0
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = 0, 0, 0, 0
    elif curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] >= 2 * Si_num:
        prev_farr = 1
        curr_counter[0], curr_counter[1], curr_counter[2], curr_counter[3] = Si_num, 0, 0, 0
        prev_counter[0], prev_counter[1], prev_counter[2], prev_counter[3] = Si_num, 0, 0, 0

    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, \
           is_react, curr_angle, curr_en, is_redepo, redepo_params