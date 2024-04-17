import numpy as np


def generate_particles(num, xsize, y_cl, y_ar_plus, y_cl_plus, T_i, T_e, y0):
    sum_y = y_cl + y_cl_plus + y_ar_plus
    curr_type = np.random.choice(3, num, p=[y_cl / sum_y, y_cl_plus / sum_y, y_ar_plus / sum_y]).reshape((-1, 1))

    num_cl = curr_type[curr_type == 0].shape[0]
    num_cl_plus = curr_type[curr_type == 1].shape[0]
    num_ar_plus = curr_type[curr_type == 2].shape[0]

    cl_particles = generate_cl(num_cl, xsize, T_i, y0)
    cl_plus_particles = generate_cl_plus(num_cl_plus, xsize, T_i/T_e, T_e, y0)
    ar_plus_particles = generate_ar_plus(num_ar_plus, xsize, T_i/T_e, T_e, y0)

    res = np.concatenate((cl_particles, cl_plus_particles, ar_plus_particles), axis=0)
    np.random.shuffle(res)
    return res


def generate_cl(num, xsize, T_i, y0):
    x = np.random.random((num, 1)) * xsize
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1))*T_i
    angle = np.random.random((num, 1)) * np.pi - np.pi * 0.5
    angle = np.where(angle < 0, angle + 2 * np.pi, angle)
    curr_type = np.ones((num, 1)) * 0
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type), axis=1)


def generate_cl_plus(num, xsize, alpha_el, T_e, y0):
    x = np.random.random((num, 1)) * xsize
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1)) * T_e
    sigma = np.arctan(np.sqrt(alpha_el))
    angle = np.random.normal(loc=0, scale=sigma, size=num).reshape((-1, 1))
    angle = np.where(angle < 0, angle + 2 * np.pi, angle)
    curr_type = np.ones((num, 1)) * 2
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type), axis=1)


def generate_ar_plus(num, xsize, alpha_el, T_e, y0):
    x = np.random.random((num, 1)) * xsize
    y = np.ones((num, 1)) * y0
    is_on_horiz = np.ones((num, 1))
    ens = np.ones((num, 1)) * T_e
    sigma = np.arctan(np.sqrt(alpha_el))
    angle = np.random.normal(loc=0, scale=sigma, size=num).reshape((-1, 1))
    angle = np.where(angle < 0, angle + 2 * np.pi, angle)
    curr_type = np.ones((num, 1)) * 3
    return np.concatenate((x, y, is_on_horiz, ens, angle, curr_type), axis=1)
