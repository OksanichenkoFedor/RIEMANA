from numba import njit
import numpy as np

@njit()
def sput_an_dep(theta):
    #return 1.0
    return 0.4 * (18.7 * np.cos(theta) - 64.7 * np.power(np.cos(theta), 2) + 145.2 * np.power(np.cos(theta), 3) -
           206 * np.power(np.cos(theta), 4) + 147.3 * np.power(np.cos(theta), 5) - 39.9 * np.power(np.cos(theta), 6))

@njit()
def ion_enh_etch_an_dep(theta):
    #return 1.0
    phi = (180.0 / np.pi) * theta
    if phi < 25:
        return 1.0
    else:
        return (90.0 - phi) / 65.0 - ((phi - 25) * (phi - 90)) / 5000



