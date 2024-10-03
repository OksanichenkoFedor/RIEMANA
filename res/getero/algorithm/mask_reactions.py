import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def mask_reaction(is_on_horiz, curr_angle):
    if is_on_horiz:
        curr_angle = np.pi - curr_angle
        if curr_angle < 0:
            curr_angle += 2.0 * np.pi
    else:
        curr_angle = 2.0 * np.pi - curr_angle

    return curr_angle