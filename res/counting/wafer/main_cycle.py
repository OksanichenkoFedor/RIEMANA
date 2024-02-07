import numpy as np
from numba import njit

from res.counting.wafer.space_orientstion import find_prev,give_next_cell

from res.counting.wafer.silicon_reactions import silicon_reaction
from res.counting.wafer.mask_reactions import mask_reaction


@njit()
def process_particles(counter_arr, is_full_arr, params_arr, Si_num, xsize, ysize, y0):
    for i in range(len(params_arr)):
        params = params_arr[i]
        unfound = True
        curr_x = params[0]
        curr_y = y0
        is_on_horiz = 1
        curr_angle = params[1]
        is_add = params[2]
        prev_y, prev_x = None, None
        while unfound:

            curr_att_x, prev_att_x, curr_att_y, prev_att_y = find_prev(curr_x, curr_y, prev_x, prev_y, curr_angle, is_on_horiz)

            if is_full_arr[curr_att_x, curr_att_y] == 1:
                # Основное вещество (идёт активная реакция)

                curr_counter = counter_arr[curr_att_x, curr_att_y]
                prev_counter = counter_arr[prev_att_x, prev_att_y]
                curr_farr = is_full_arr[curr_att_x, curr_att_y]
                prev_farr = is_full_arr[prev_att_x, prev_att_y]

                curr_counter, prev_counter, curr_farr, prev_farr = silicon_reaction(is_add, curr_counter, prev_counter,
                                                                                    curr_farr, prev_farr, Si_num)

                counter_arr[curr_att_x, curr_att_y] = curr_counter
                counter_arr[prev_att_x, prev_att_y] = prev_counter
                is_full_arr[curr_att_x, curr_att_y] = curr_farr
                is_full_arr[prev_att_x, prev_att_y] = prev_farr

                unfound = False

            elif is_full_arr[curr_att_x, curr_att_y] == 2:
                # Маска

                curr_angle = mask_reaction(is_on_horiz, curr_angle)
            else:
                prev_x = curr_x
                prev_y = curr_y
                prev_horiz = is_on_horiz
                prev_angle = curr_angle

                curr_x, curr_y, curr_angle, is_on_horiz = give_next_cell(prev_x, prev_y, prev_angle, prev_horiz)

                if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                    unfound = False
                elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                    unfound = False



