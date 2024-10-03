import numpy as np

from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angle, isotropic_retraction):
    #print()

    is0 = is_full_arr[curr_x + 0, curr_y + 1]
    is1 = is_full_arr[curr_x + 1, curr_y + 0]
    is2 = is_full_arr[curr_x + 0, curr_y - 1]
    is3 = is_full_arr[curr_x - 1, curr_y + 0]

    num = int(is0) + int(is1) + int(is2) + int(is3)

    quarter = int((((angle / np.pi) * 4.0 + 5.0) % 8.0) * 0.5)
    quarter1 = int((quarter + 2) % 4)
    if quarter1 == 0:
        x_end, y_end = 0, 1
    elif quarter1 == 1:
        x_end, y_end = 1, 0
    elif quarter1 == 2:
        x_end, y_end = 0, -1
    elif quarter1 == 3:
        x_end, y_end = -1, 0
    else:
        print("Incorrect quarter retract_cell: ", quarter1)

    if isotropic_retraction:
        if is0:
            counter_arr[:, curr_x + 0, curr_y + 1] += counter_arr[:, curr_x, curr_y] // num
        if is1:
            counter_arr[:, curr_x + 1, curr_y + 0] += counter_arr[:, curr_x, curr_y] // num
        if is2:
            counter_arr[:, curr_x + 0, curr_y - 1] += counter_arr[:, curr_x, curr_y] // num
        if is3:
            counter_arr[:, curr_x - 1, curr_y + 0] += counter_arr[:, curr_x, curr_y] // num
        counter_arr[:, curr_x + x_end, curr_y + y_end] += counter_arr[:, curr_x, curr_y]-num*(counter_arr[:, curr_x, curr_y] // num)
    else:
        if is_full_arr[curr_x + x_end, curr_y + y_end]!=1.0:
            print("Incorrect retract_cell: ", angle/np.pi, quarter1, is0, is1, is2, is3)
        counter_arr[:, curr_x + x_end, curr_y + y_end] += counter_arr[:, curr_x, curr_y]
    is_full_arr[curr_x, curr_y] = 0
    counter_arr[0, curr_x, curr_y] = 0
    counter_arr[1, curr_x, curr_y] = 0
    counter_arr[2, curr_x, curr_y] = 0
    counter_arr[3, curr_x, curr_y] = 0