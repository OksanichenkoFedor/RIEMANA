from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angle, isotropic_retraction):
    #print()
    counter_arr[0, curr_x, curr_y] = 0
    counter_arr[1, curr_x, curr_y] = 0
    counter_arr[2, curr_x, curr_y] = 0
    counter_arr[3, curr_x, curr_y] = 0