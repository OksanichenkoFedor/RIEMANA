import numpy as np
from numba import njit

from res.getero.algorithm.space_orientation import find_prev, give_next_cell

from res.getero.algorithm.mask_reactions import mask_reaction

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction

from res.getero.algorithm.dynamic_profile import delete_point


def test_silicon_reaction(is_add, curr_counter, prev_counter, curr_farr, prev_farr, Si_num):
    # Основное вещество (идёт активная реакция)
    if is_add:
        curr_counter += 1
        #print("Села")
    else:
        curr_counter -= 1
        #print("Выбила")
    if curr_counter <= 0:
        curr_farr = 0
        curr_counter = 0

    elif curr_counter >= 2 * Si_num:
        prev_farr = 1
        curr_counter = Si_num
        prev_counter = Si_num

    return curr_counter, prev_counter, curr_farr, prev_farr


def process_one_particle(counter_arr, is_full_arr, border_layer_arr, params, Si_num, xsize, ysize, R, otn_const):
    arr_x, arr_y, rarr_x, rarr_y = [], [], [], []
    curr_x = params[0]
    curr_y = params[1]
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    prev_y, prev_x = None, None
    unfound = True
    changed_angle = False
    #if curr_type == 6:
    #    print("Start")
    while unfound:

        #if curr_type == 6:
        #    print("Start1")
        curr_att_x, prev_att_x, curr_att_y, prev_att_y = find_prev(curr_x, curr_y, prev_x, prev_y, curr_angle,
                                                                   is_on_horiz)
        if (curr_att_x == prev_att_x and curr_att_y == prev_att_y) and (not (prev_y is None)):
            pass
            print("F[neyu!!!!")
            print(curr_x, curr_y, prev_x, prev_y)
            print(curr_att_x, prev_att_x, curr_att_y, prev_att_y)
            print(curr_angle, curr_angle / np.pi)
            print(is_full_arr[curr_att_x, curr_att_y])
        if is_full_arr[curr_att_x, curr_att_y] == 1.0:
            #if curr_type == 6:
            #    print("React",is_full_arr[curr_att_x, curr_att_y], counter_arr[:, curr_att_x, curr_att_y])
            # Основное вещество (идёт активная реакция)

            curr_counter = counter_arr[:, curr_att_x, curr_att_y]
            prev_counter = counter_arr[:, prev_att_x, prev_att_y]
            curr_farr = is_full_arr[curr_att_x, curr_att_y]
            prev_farr = is_full_arr[prev_att_x, prev_att_y]

            if curr_counter[0]+curr_counter[1]+curr_counter[2]+curr_counter[3] == 0:
                print("---")
                print("Пустая не пустая!!!")
                print(curr_att_x, curr_att_y)
                print("---")
            new_type, new_curr_counter, new_prev_counter, new_curr_farr, new_prev_farr, is_react, new_angle, \
            new_en, is_redepo, redepo_params = silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr,
                                                                prev_farr, Si_num, is_on_horiz, curr_angle, curr_en,
                                                                R, otn_const)

            #ind = find_index(border_layer, curr_att_x, curr_att_y)
            #print("Index in border layer: ",ind)

            if new_curr_farr!=curr_farr:
                #удаление
                #0 - внутри
                #1 - граница
                #-1 - снаружи
                delete_point(border_layer_arr, curr_att_x, curr_att_y)
                if new_curr_farr:
                    print("Непредсказуемое удаление!!!")
                #border_layer_arr[curr_att_x, curr_att_y, 0] = -1.0
                #if curr_att_x>0:
                #    if border_layer_arr[curr_att_x - 1, curr_att_y, 0] == 0:
                #        border_layer_arr[curr_att_x - 1, curr_att_y, 0] = 1.0
                #if curr_att_x<xsize-1:
                #    if border_layer_arr[curr_att_x + 1, curr_att_y, 0] == 0:
                #        border_layer_arr[curr_att_x + 1, curr_att_y, 0] = 1.0
                #if curr_att_y>0:
                #    if border_layer_arr[curr_att_x, curr_att_y - 1, 0] == 0:
                #        border_layer_arr[curr_att_x, curr_att_y - 1, 0] = 1.0
                #if curr_att_y<ysize-1:
                #    if border_layer_arr[curr_att_x, curr_att_y + 1, 0] == 0:
                #        border_layer_arr[curr_att_x, curr_att_y + 1, 0] = 1.0

            if new_prev_farr!=prev_farr:
                #восстановление частицы
                print("Восстановление, код нёедописан!!!")
                #TODO допилить нормальное востановление частицы(надо барать из граничных точек ту, которая вошла вовнутрь)
                if new_prev_farr == 0:
                    print("Непредсказуемое восстановление!!!")
                border_layer_arr[curr_att_x, curr_att_y, 0] = 1.0
            counter_arr[:, curr_att_x, curr_att_y] = new_curr_counter
            counter_arr[:, prev_att_x, prev_att_y] = new_prev_counter
            is_full_arr[curr_att_x, curr_att_y] = new_curr_farr
            is_full_arr[prev_att_x, prev_att_y] = new_prev_farr
            curr_angle = new_angle
            curr_type = new_type
            curr_en = new_en

            if is_redepo:
                redepo_params[0] = curr_x
                redepo_params[1] = curr_y
                redepo_params[2] = is_on_horiz
                arr_x_1, arr_y_1, arr_x_2, arr_y_2 = process_one_particle(counter_arr, is_full_arr,  border_layer_arr,
                                                                    redepo_params, Si_num, xsize, ysize, R, otn_const)
                rarr_x = rarr_x + arr_x_1 + arr_x_2
                rarr_y = rarr_y + arr_y_1 + arr_y_2



            if is_react:
                unfound = False
            else:
                changed_angle = True

        elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
            # Маска
            curr_angle = mask_reaction(is_on_horiz, curr_angle)
            changed_angle = True
        else:
            prev_x = curr_x
            prev_y = curr_y

            curr_x, curr_y, new_angle, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

            arr_x.append(curr_x - 0.5)
            arr_y.append(curr_y - 0.5)

            curr_angle = new_angle
            is_on_horiz = new_is_on_horiz

            if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                unfound = False
            elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                unfound = False

        if changed_angle:
            prev_x = curr_x
            prev_y = curr_y

            curr_x, curr_y, new_angle, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

            arr_x.append(curr_x - 0.5)
            arr_y.append(curr_y - 0.5)

            curr_angle = new_angle
            is_on_horiz = new_is_on_horiz

            if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                unfound = False
            elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                unfound = False
            changed_angle = False
    return arr_x, arr_y, rarr_x, rarr_y


def process_particles(counter_arr, is_full_arr, border_layer,  params_arr, Si_num, xsize, ysize, y0, R, otn_const):
    arr_x, arr_y, rarr_x, rarr_y = [], [], [], []
    for i in range(len(params_arr)):
        curr_x = params_arr[i][0]
        curr_y = y0
        is_on_horiz = 1
        curr_en = params_arr[i][1]
        curr_angle = params_arr[i][2]
        curr_type = params_arr[i][3]
        curr_params_arr = [curr_x, curr_y, is_on_horiz, curr_en, curr_angle, curr_type]

        arr_x_1, \
        arr_y_1, rarr_x_1, rarr_y_1 = process_one_particle(counter_arr, is_full_arr, border_layer,  curr_params_arr,
                                                           Si_num, xsize, ysize, R, otn_const)
        arr_x = arr_x + arr_x_1
        arr_y = arr_y + arr_y_1
        rarr_x = rarr_x + rarr_x_1
        rarr_y = rarr_y + rarr_y_1

    return counter_arr, is_full_arr, arr_x, arr_y, rarr_x, rarr_y


def test_process_particles(counter_arr, is_full_arr, border_layer, params_arr, Si_num, xsize, ysize, y0, axis):
    for i in range(len(params_arr)):
        params = params_arr[i]
        unfound = True
        curr_x = params[0]
        curr_en = params[1]
        curr_y = y0
        is_on_horiz = 1
        curr_angle = params[2]
        is_add = params[3]
        prev_y, prev_x = None, None
        arr_x, arr_y = [], []
        prev_angle = curr_angle
        changed_angle = False
        while unfound:
            print(curr_angle/np.pi)
            curr_att_x, prev_att_x, curr_att_y, prev_att_y = find_prev(curr_x, curr_y, prev_x, prev_y, curr_angle, is_on_horiz)
            if curr_att_x==prev_att_x and curr_att_y==prev_att_y and prev_y!=None:
                print("Ахтунг!!!!")
                print(curr_x, curr_y, prev_x, prev_y)
                print(curr_att_x, prev_att_x, curr_att_y, prev_att_y)
                print(curr_angle, curr_angle / np.pi)
                if prev_angle!=None:
                    print(prev_angle, prev_angle / np.pi)
                #print(is_full_arr[curr_att_x, curr_att_y])
                print("--")
            if is_full_arr[curr_att_x, curr_att_y] == 1.0:
                # Основное вещество (идёт активная реакция)
                curr_counter = counter_arr[0, curr_att_x, curr_att_y]
                prev_counter = counter_arr[0, prev_att_x, prev_att_y]

                curr_farr = is_full_arr[curr_att_x, curr_att_y]
                prev_farr = is_full_arr[prev_att_x, prev_att_y]

                curr_counter, prev_counter, curr_farr, prev_farr = test_silicon_reaction(is_add, curr_counter, prev_counter,
                                                                                    curr_farr, prev_farr, Si_num)

                prev_angle = curr_angle
                counter_arr[0, curr_att_x, curr_att_y] = curr_counter
                counter_arr[0, prev_att_x, prev_att_y] = prev_counter
                is_full_arr[curr_att_x, curr_att_y] = curr_farr
                is_full_arr[prev_att_x, prev_att_y] = prev_farr

                unfound = False


            elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
                # Маска
                curr_angle = mask_reaction(is_on_horiz, curr_angle)
                changed_angle = True
            else:
                prev_x = curr_x
                prev_y = curr_y
                #prev_horiz = is_on_horiz


                curr_x, curr_y, new_angle, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

                #axis.plot([], [curr_y], 'o', color="k")
                arr_x.append(curr_x-0.5)
                arr_y.append(curr_y-0.5)
                prev_angle = curr_angle
                curr_angle = new_angle
                is_on_horiz = new_is_on_horiz

                if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                    unfound = False
                elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                    unfound = False

            if changed_angle:
                prev_x = curr_x
                prev_y = curr_y
                # prev_horiz = is_on_horiz

                curr_x, curr_y, new_angle, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

                # axis.plot([], [curr_y], 'o', color="k")
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)
                prev_angle = curr_angle
                curr_angle = new_angle
                is_on_horiz = new_is_on_horiz

                if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                    unfound = False
                elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                    unfound = False

                changed_angle = False

    return counter_arr, is_full_arr, arr_x, arr_y