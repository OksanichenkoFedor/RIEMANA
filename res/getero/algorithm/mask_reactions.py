import numpy as np
from numba import njit

@njit()
def mask_reaction(is_on_horiz, curr_angle):
    if is_on_horiz:
        curr_angle = np.pi - curr_angle
        if curr_angle < 0:
            curr_angle += 2.0 * np.pi
    else:
        curr_angle = 2.0 * np.pi - curr_angle

    return curr_angle