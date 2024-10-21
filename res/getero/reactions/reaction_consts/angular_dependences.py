from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def sput_an_dep(theta):
    if theta<0 or theta>np.pi*0.5:
        print("sput_an_dep плохой угол:", (180.0 / np.pi) * np.abs(theta))
        theta = np.pi * 0.5
        #if theta>np.pi and theta<2*np.pi:
        #    theta
    return 0.4 * (18.7 * np.cos(theta) - 64.7 * np.power(np.cos(theta), 2) + 145.2 * np.power(np.cos(theta), 3) -
           206 * np.power(np.cos(theta), 4) + 147.3 * np.power(np.cos(theta), 5) - 39.9 * np.power(np.cos(theta), 6))

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def ion_enh_etch_an_dep(theta):
    if theta<0 or theta>np.pi*0.5:
        print("ion_enh_etch_an_dep плохой угол:", (180.0 / np.pi) * np.abs(theta))
        theta = np.pi * 0.5
    phi = (180.0 / np.pi) * np.abs(theta)
    if phi < 25:
        return 1.0
    else:
        return (90.0 - phi) / 65.0 - ((phi - 25) * (phi - 90)) / 5000



