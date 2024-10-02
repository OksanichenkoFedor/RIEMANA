import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
from res.utils.config import min_throw_away_angle

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def give_mnk(x, y):
    dim = 2
    tp = np.abs(np.max(y) - np.min(y)) > np.abs(np.max(x) - np.min(x))
    if tp:
        x, y = y, x
    x = x.reshape((x.shape[0], 1))
    y = y.reshape((y.shape[0], 1))

    X = np.ones((x.shape[0], dim + 1))

    for k in range(1, dim + 1):
        X[:, k] = x[:, 0] ** k

    # Вычисляем столбец коэффицентов регрессии

    w = np.linalg.pinv(X) @ y
    c, b, a = w[:, 0]
    return c, b, a, tp


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_angle(delta_x, delta_y):
    if np.abs(delta_x) < 10 ** (-5):
        if delta_y > 0:
            return np.pi / 2
        else:
            return 1.5 * np.pi
    if np.abs(delta_y) < 10 ** (-5):
        if delta_x > 0:
            return 0
        else:
            return np.pi
    if delta_x > 0:
        if delta_y > 0:
            # I-quarter
            return np.arctan(delta_y / delta_x)
        else:
            # VI-quarter
            return 2.0 * np.pi - np.arctan(((-1.0) * delta_y) / delta_x)

    else:
        if delta_y > 0:
            # II-quarter
            return 0.5 * np.pi + np.arctan(((-1.0) * delta_x) / delta_y)
        else:
            # III-quarter
            return np.pi + np.arctan(delta_y / delta_x)


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_angle_collision(old_angle, new_angle, curr_segment, cross_vec):
    is_oob = False
    res_angle = new_angle
    left_angle = count_angle(curr_segment[0, 1] - curr_segment[1, 1], curr_segment[0, 0] - curr_segment[1, 0])
    right_angle = count_angle(curr_segment[1, 1] - curr_segment[0, 1], curr_segment[1, 0] - curr_segment[0, 0])
    simple_norm_angle = count_norm_angle(curr_segment[0, 0], curr_segment[0, 1], curr_segment[1, 0],
                                                 curr_segment[1, 1])
    if np.abs(((right_angle-left_angle)%(2*np.pi))/np.pi-1.0)>10**(-5):
        print("Incorrect base vectors check_angle_collision: ", left_angle/np.pi, right_angle/np.pi)
        return is_oob, left_angle, right_angle, None
    if (new_angle-right_angle)%(2*np.pi)>np.pi:
        is_oob = True
        #res_angle = simple_norm_angle
        if (old_angle-right_angle)%(2*np.pi)>1.5*np.pi:
            res_angle = (right_angle+np.random.random()*min_throw_away_angle)%(2*np.pi)
        else:
            res_angle = (left_angle-np.random.random()*min_throw_away_angle)%(2*np.pi)

    return is_oob, left_angle, right_angle, res_angle
    #print()


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_norm_angle(x1, y1, x2, y2):
    # Пустота всегда слева от линии поэтому мы всегда явно можем определить угол от нормали.
    # Он будет улгом вектора ребра + 90.
    delta_x, delta_y = x2 - x1, y2 - y1
    cos = delta_y / np.sqrt(delta_x * delta_x + delta_y * delta_y)
    sin = delta_x / np.sqrt(delta_x * delta_x + delta_y * delta_y)
    if cos >= 0 and sin >= 0:
        # первая четверть
        angle = np.arccos(cos)
    elif cos < 0 and sin >= 0:
        # вторая четверть
        angle = np.pi - np.arcsin(sin)
    elif cos < 0 and sin < 0:
        # третья четверть
        angle = np.pi + np.arccos((-1.0) * cos)
    elif cos >= 0 and sin < 0:
        # четвёртая четверть
        angle = (-1.0) * np.arccos(cos)
    angle = angle + np.pi * 0.5
    return angle