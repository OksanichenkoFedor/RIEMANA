from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numpy as np
import res.utils.config as config


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def custom_choise(Ps):
    # np.random.seed(config.seed)
    num = np.random.random()
    sum = 0
    for i in range(len(Ps)):
        sum += Ps[i]
        if num <= sum:
            return i


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def straight_reflection(curr_angle, n_angle):
    angle = 2 * n_angle - (curr_angle + np.pi)
    return angle%(2.0*np.pi)


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def generate_cos_point():
    # np.random.seed(config.seed)
    a = 2.0 * np.random.random() - 1.0

    # по синусу
    x = np.arccos(a)
    if x>np.pi/2:
       return x-np.pi

    # по косинусу
    #x = np.arcsin(a)

    # равномерное
    #x = a*np.pi*0.5

    return x


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_falling_angle(start_angle, normal_angle):
    curr_angle = np.abs(normal_angle - (np.pi + start_angle))
    if curr_angle > np.pi * 0.5:
        curr_angle = np.abs(2 * np.pi - curr_angle)
    if curr_angle > np.pi * 0.5:
        #print("В расчёт угла падения передан некорректный угол: ", (180.0 / np.pi) * np.abs(start_angle),
        #      (180.0 / np.pi) * np.abs(normal_angle))
        curr_angle = 0
    return curr_angle

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def isotropic_reflection(curr_angle, n_angle):
    # return straight_reflection(curr_angle, n_angle)
    dop_angle = generate_cos_point()
    angle = n_angle + dop_angle
    if angle > 2 * np.pi:
        angle -= 2.0 * np.pi

    if angle < 0:
        angle += 2.0 * np.pi
    return angle
    # if is_on_horiz:
    #    if curr_angle<np.pi*0.5 or curr_angle>np.pi*1.5:
    #        return np.pi + dop_angle
    #    else:
    #        if dop_angle<0:
    #            return dop_angle+2*np.pi
    #        else:
    #            return dop_angle
    # else:
    #    if curr_angle<np.pi:
    #        return np.pi*1.5 + dop_angle
    #    else:
    #        return np.pi*0.5 + dop_angle
