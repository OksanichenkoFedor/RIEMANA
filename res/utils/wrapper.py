from numba import jit

def clever_njit(do_njit=True, cache=False, parallel=True):
    def actual_wr(funk):
        if do_njit:
            return jit(funk, nopython=True, cache=cache, parallel=parallel)
        else:
            return funk
    return actual_wr