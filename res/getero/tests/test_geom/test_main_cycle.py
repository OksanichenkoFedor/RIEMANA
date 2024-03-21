import numpy as np
from numba import njit

from res.getero.algorithm.space_orientation import find_prev, give_next_cell

from res.getero.algorithm.mask_reactions import mask_reaction


def silicon_reaction(is_add, curr_counter, prev_counter, curr_farr, prev_farr, Si_num):
    # Основное вещество (идёт активная реакция)
    if is_add:
        curr_counter += 1
        # print("Села")
    else:
        curr_counter -= 1
        # print("Выбила")
    if curr_counter <= 0:
        curr_farr = 0
        curr_counter = 0

    elif curr_counter >= 2 * Si_num:
        prev_farr = 1
        curr_counter = Si_num
        prev_counter = Si_num

    return curr_counter, prev_counter, curr_farr, prev_farr


def test_process_particles(counter_arr, is_full_arr, params_arr, Si_num, xsize, ysize, y0, axis):
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

                curr_counter, prev_counter, curr_farr, prev_farr = silicon_reaction(is_add, curr_counter, prev_counter,
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