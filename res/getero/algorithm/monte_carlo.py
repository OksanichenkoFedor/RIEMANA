import numpy as np
import res.utils.config as config
from res.getero.algorithm.utils import generate_cos_point
import matplotlib.pyplot as plt
np.random.seed(config.seed)


def generate_particles(num, xsize, y_cl, y_ar_plus, y_cl_plus, T_i, T_e, y0, seed=None):
    if seed != None:
        np.random.seed(seed)
    sum_y = y_cl + y_cl_plus + y_ar_plus
    curr_type = np.random.choice(3, num, p=[y_cl / sum_y, y_cl_plus / sum_y, y_ar_plus / sum_y]).reshape((-1, 1))

    num_cl = curr_type[curr_type == 0].shape[0]
    num_cl_plus = curr_type[curr_type == 1].shape[0]
    num_ar_plus = curr_type[curr_type == 2].shape[0]

    cl_particles = generate_cl(num_cl, xsize, T_i, y0, seed)
    cl_plus_particles = generate_cl_plus(num_cl_plus, xsize, T_i/T_e, T_e, y0, seed)
    ar_plus_particles = generate_ar_plus(num_ar_plus, xsize, T_i/T_e, T_e, y0, seed)

    res = np.concatenate((cl_particles, cl_plus_particles, ar_plus_particles), axis=0)
    if seed != None:
        np.random.seed(seed)
    np.random.shuffle(res)
    return res


def generate_cl(num, xsize, T_i, y0, seed):
    if seed != None:
        np.random.seed(seed)
    x = np.random.random((num, 1)) * xsize + 1.0
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1))*T_i
    angle = []
    for i in range(num):
        angle.append(generate_cos_point())
    angle = np.array(angle).reshape((num, 1))

    #angle = np.random.random((num, 1)) * np.pi - np.pi * 0.5

    angle = np.where(angle < 0, angle + 2 * np.pi, angle)

    curr_type = np.ones((num, 1)) * 0
    start_y = y.copy()
    start_x = (x.copy()).astype(int)
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type, start_x, start_y), axis=1)


def generate_cl_plus(num, xsize, alpha_el, T_e, y0, seed):
    if seed != None:
        np.random.seed(seed)
    x = np.random.random((num, 1)) * xsize + 1.0
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1)) * T_e
    sigma = np.arctan(np.sqrt(alpha_el))
    angle = np.random.normal(loc=0, scale=sigma, size=num).reshape((-1, 1))
    angle = np.where(angle < 0, angle + 2 * np.pi, angle)
    curr_type = np.ones((num, 1)) * 2
    start_y = y.copy()
    start_x = (x.copy()).astype(int)
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type, start_x, start_y), axis=1)


def generate_ar_plus(num, xsize, alpha_el, T_e, y0, seed):
    if seed != None:
        np.random.seed(seed)
    x = np.random.random((num, 1)) * xsize + 1.0
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1)) * T_e
    sigma = np.arctan(np.sqrt(alpha_el))
    angle = np.random.normal(loc=0, scale=sigma, size=num).reshape((-1, 1))
    angle = np.where(angle < 0, angle + 2 * np.pi, angle)
    curr_type = np.ones((num, 1)) * 3
    start_y = y.copy()
    start_x = (x.copy()).astype(int)
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type, start_x, start_y), axis=1)
