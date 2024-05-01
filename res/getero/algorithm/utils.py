from numba import jit, njit
import numpy as np
import res.utils.config as config



@njit()
def custom_choise(Ps):
    #np.random.seed(config.seed)
    num = np.random.random()
    sum = 0
    for i in range(len(Ps)):
        sum+=Ps[i]
        if num<=sum:
            return i

@njit()
def straight_reflection(curr_angle, is_on_horiz):
    angle = curr_angle
    if is_on_horiz:
        angle = np.pi - angle
        if angle < 0:
            angle += 2.0 * np.pi
    else:
        angle = 2.0 * np.pi - angle
    return angle

@njit()
def generate_cos_point():
    #np.random.seed(config.seed)
    a = 2*np.random.random()-1
    x = np.arcsin(a)
    return x

@njit()
def isotropic_reflection(curr_angle, is_on_horiz):
    dop_angle = generate_cos_point()
    if is_on_horiz:
        if curr_angle<np.pi*0.5 or curr_angle>np.pi*1.5:
            return np.pi + dop_angle
        else:
            if dop_angle<0:
                return dop_angle+2*np.pi
            else:
                return dop_angle
    else:
        if curr_angle<np.pi:
            return np.pi*1.5 + dop_angle
        else:
            return np.pi*0.5 + dop_angle