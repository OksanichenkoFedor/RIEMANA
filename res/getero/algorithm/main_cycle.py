import numpy as np
from numba import njit
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numba as nb

from res.getero.algorithm.space_orientation import find_next, give_next_cell, throw_particle_away

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.mask_reactions import mask_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr, params, Si_num, xsize, ysize, R, test,
                         old_changed_angle, max_value):
    # print("Start process")
    arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                       nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    curr_x = params[0]
    curr_y = params[1]
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    prev_att_x = int(params[6])
    prev_att_y = int(params[7])
    prev_y, prev_x = None, None
    unfound = True
    changed_angle = False
    num = 0
    unfound_test = True
    not_max_value = True
    #print("---------")
    Prev_x = nb.typed.List.empty_list(nb.f8)
    Prev_y = nb.typed.List.empty_list(nb.f8)
    p_a_x = nb.typed.List.empty_list(nb.f8)
    p_a_y = nb.typed.List.empty_list(nb.f8)
    Curr_x = nb.typed.List.empty_list(nb.f8)
    Curr_y = nb.typed.List.empty_list(nb.f8)
    c_a_x = nb.typed.List.empty_list(nb.f8)
    c_a_y = nb.typed.List.empty_list(nb.f8)
    ifa_p = nb.typed.List.empty_list(nb.f8)
    ifa_c = nb.typed.List.empty_list(nb.f8)
    while unfound and not_max_value:

        if max_value != -1.0:
            if num > max_value:
                not_max_value = False
        num += 1
        curr_att_x, curr_att_y = find_next(curr_x, curr_y, prev_x, prev_y, prev_att_x, prev_att_y)
        #print("---")
        if prev_x is None:
            Prev_x.append(0)
            Prev_y.append(0)
        else:
            Prev_x.append(prev_x)
            Prev_y.append(prev_y)
        p_a_x.append(prev_att_x)
        p_a_y.append(prev_att_y)
        Curr_x.append(curr_x)
        Curr_y.append(curr_y)
        c_a_x.append(curr_att_x)
        c_a_y.append(curr_att_y)
        ifa_p.append(is_full_arr[prev_att_x, prev_att_y])
        ifa_c.append(is_full_arr[curr_att_x, curr_att_y])
        #print(prev_att_x, prev_att_y, prev_x, prev_y)
        #print(curr_att_y, curr_att_y, curr_x, curr_y)
        #print(is_full_arr[curr_att_x, curr_att_y], is_full_arr[prev_att_x, prev_att_y])
        #print(prev_x, prev_y)
        if curr_type == 9.0:
            pass
            # print("---")
            # print(curr_att_x, curr_att_y)
            # print(curr_x, curr_y)
            # print(is_full_arr[curr_att_x, curr_att_y])
        if (curr_att_x == prev_att_x and curr_att_y == prev_att_y) and (not (prev_y is None)):
            pass
            print("Ахтунг!!!!")
            print(curr_x, curr_y, prev_x, prev_y)
            print(curr_att_x, prev_att_x, curr_att_y, prev_att_y)
            print(curr_angle, curr_angle / np.pi)
            print(is_full_arr[curr_att_x, curr_att_y])
        # print(curr_att_x, curr_att_y)
        if is_full_arr[curr_att_x, curr_att_y] == 1.0:
            if (num > 10000 and unfound_test):
                if curr_type==9.0:
                    print("Argon in cage!")
                    return arr_x, arr_y, rarr_x, rarr_y
                else:
                    print("Starange: ", curr_type)
                    print([curr_x, curr_y, is_on_horiz, curr_en, curr_angle, curr_type, prev_att_x, prev_att_y])
                    unfound_test = False
            # print("---")
            # print("Reaction")
            # print(curr_x, curr_y)
            # print(curr_att_x, curr_att_y)
            # print("Start reaction")
            # Основное вещество (идёт активная реакция)
            # print("---")
            # print("Reaction: ", curr_type)
            # print()
            curr_counter = counter_arr[:, curr_att_x, curr_att_y]
            prev_counter = counter_arr[:, prev_att_x, prev_att_y]
            curr_farr = is_full_arr[curr_att_x, curr_att_y]
            prev_farr = is_full_arr[prev_att_x, prev_att_y]
            # print(curr_att_x, curr_att_y)
            # print("curr_counter: ",curr_counter)
            # print("curr_farr: ",curr_farr)
            # print(curr_angle/np.pi,is_on_horiz)
            # print("---")
            if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] == 0:
                print("---")
                print("Пустая не пустая!!!")
                print(curr_att_x, curr_att_y)
                print("---")
            new_type, new_curr_counter, new_prev_counter, new_curr_farr, new_prev_farr, is_react, new_angle, \
            new_en, is_redepo, redepo_params = silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr,
                                                                prev_farr, Si_num, is_on_horiz, curr_angle, curr_en,
                                                                R)

            if new_curr_farr != curr_farr:
                # удаление
                # 0 - внутри
                # 1 - граница
                # -1 - снаружи
                print("Delete: ", curr_att_x, curr_att_y)
                delete_point(border_layer_arr, curr_att_x, curr_att_y)
                if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
                    print("Удаление не произведено!")
                if new_curr_farr:
                    print("Непредсказуемое удаление!!!")

            if new_prev_farr != prev_farr:
                # восстановление частицы
                print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
                create_point(border_layer_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)
            counter_arr[:, curr_att_x, curr_att_y] = new_curr_counter
            counter_arr[:, prev_att_x, prev_att_y] = new_prev_counter
            is_full_arr[curr_att_x, curr_att_y] = new_curr_farr
            is_full_arr[prev_att_x, prev_att_y] = new_prev_farr
            curr_angle = new_angle
            curr_type = new_type
            curr_en = new_en

            if is_redepo:
                # print("Start redepo")
                redepo_params[0] = curr_x
                redepo_params[1] = curr_y
                redepo_params[2] = is_on_horiz
                redepo_params[4] = redepo_params[4] / np.pi
                redepo_params[6] = prev_att_x
                redepo_params[7] = prev_att_y
                # print("old_angle: ", old_angle/np.pi)
                # print(redepo_params)
                redepo_params[4] = redepo_params[4] * np.pi
                if test:
                    arr_x_1, arr_y_1, arr_x_2, arr_y_2 = process_one_particle(counter_arr, is_full_arr,
                                                                              border_layer_arr, redepo_params, Si_num,
                                                                              xsize, ysize, R, True, True, max_value)

                    rarr_x = unite_lists(unite_lists(rarr_x, arr_x_1), arr_x_2)
                    rarr_y = unite_lists(unite_lists(rarr_y, arr_y_1), arr_y_2)

                else:
                    process_one_particle(counter_arr, is_full_arr, border_layer_arr, redepo_params, Si_num, xsize,
                                         ysize, R, False, True, max_value)
                # print("End redepo")
                if is_full_arr[prev_att_x,prev_att_y]==1:
                    print("Ловушка джокера")
                    prev_att_x, prev_att_y, curr_x, curr_y = throw_particle_away(is_full_arr, prev_att_x, prev_att_y,
                                                                                 curr_x, curr_y)

            if is_react:
                unfound = False
            else:
                changed_angle = True

            # print("End reaction")

        elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
            # print("Mask: ", curr_type)
            # print(curr_angle)
            # Маска
            curr_angle = mask_reaction(is_on_horiz, curr_angle)
            changed_angle = True
            # print(curr_angle)
        else:
            #print("---")
            #print("Move")
            #print(curr_x, curr_y)
            #print(curr_att_x, curr_att_y)
            # print("Start move")
            # print("Move: ", curr_type)
            # print(curr_att_x, curr_att_y)
            # print("curr_farr: ",is_full_arr[curr_att_x, curr_att_y])
            if border_layer_arr[curr_att_x, curr_att_y, 0] != -1:
                pass
                # print("Некорректный расчёт профиля! ",border_layer_arr[curr_att_x, curr_att_y, 0])
            prev_x = curr_x
            prev_y = curr_y
            prev_att_x, prev_att_y = curr_att_x, curr_att_y

            curr_x, curr_y, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

            if test:
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)

            is_on_horiz = new_is_on_horiz

            if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                unfound = False
            elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                unfound = False
            # print("End move")

        if changed_angle:

            if (is_full_arr[prev_att_x, prev_att_y] and unfound_test):
                print("Everlasting reaction")
                for i in range(len(Prev_x)):
                    print("---")
                    print(Prev_x[i], Prev_y[i], p_a_x[i], p_a_y[i])
                    print(Curr_x[i], Curr_y[i], c_a_x[i], c_a_y[i])
                    print(ifa_p[i], ifa_c[i])
                print("После отражения мы внутри!!! ", curr_type)
                print(prev_att_x, prev_att_y)
                print(curr_att_y, curr_att_y)
                print(prev_x, prev_y)
                print([curr_x, curr_y, is_on_horiz, curr_en, curr_angle, curr_type, prev_att_x, prev_att_y])
                print([params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]])
                unfound_test = False

            prev_x, prev_y = None, None

            # prev_x = curr_x
            # prev_y = curr_y
            #prev_att_x, prev_att_y = curr_att_x, curr_att_y
            #
            # curr_x, curr_y, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)
            # prev_att_x, prev_att_y = find_next(curr_x, curr_y, prev_x, prev_y, prev_att_x, prev_att_y)
            #
            if test:
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)
            #
            # is_on_horiz = new_is_on_horiz
            #
            # if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
            #    unfound = False
            # elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
            #    unfound = False
            changed_angle = False
    # print(num)
    # print("End process")
    if test:
        return arr_x, arr_y, rarr_x, rarr_y


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_particles(counter_arr, is_full_arr, border_layer_arr, params_arr, Si_num, xsize, ysize, R, test,
                      max_value=-1.0):
    if test:
        arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                       nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    for i in range(len(params_arr)):
        curr_params_arr = params_arr[i]
        if test:
            arr_x_1, arr_y_1, rarr_x_1, rarr_y_1 = \
                process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                                     curr_params_arr, Si_num, xsize, ysize, R, True, False, max_value)

            arr_x = unite_lists(arr_x, arr_x_1)
            arr_y = unite_lists(arr_y, arr_y_1)
            rarr_x = unite_lists(rarr_x, rarr_x_1)
            rarr_y = unite_lists(rarr_y, rarr_y_1)
        else:
            process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                                 curr_params_arr, Si_num, xsize, ysize, R, False, False, max_value)
    if test:
        return arr_x, arr_y, rarr_x, rarr_y


@njit()
def unite_lists(a, b):
    for i in range(len(b)):
        a.append(b[i])
    return a
