from numba import njit
import numpy as np

@njit()
def custom_choise(Ps):
    #print(Ps)
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