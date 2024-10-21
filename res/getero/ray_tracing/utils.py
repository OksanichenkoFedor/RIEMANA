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
def check_if_part_inside(old_angle, curr_segment):
    right_angle = count_angle(curr_segment[1, 1] - curr_segment[0, 1], curr_segment[1, 0] - curr_segment[0, 0])
    delta = (right_angle - old_angle)/np.pi
    if delta<0:
        delta+=2
    delta = delta%2
    if delta>1:
        return True
    return False

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_angle_collision(old_angle, new_angle, curr_segment, cross_vec, seed):
    is_oob = False
    res_angle = new_angle
    left_angle = count_angle(curr_segment[0, 1] - curr_segment[1, 1], curr_segment[0, 0] - curr_segment[1, 0])
    right_angle = count_angle(curr_segment[1, 1] - curr_segment[0, 1], curr_segment[1, 0] - curr_segment[0, 0])

    if np.abs(((right_angle-left_angle)%(2*np.pi))/np.pi-1.0)>10**(-5):
        print("Incorrect base vectors check_angle_collision: ", left_angle/np.pi, right_angle/np.pi)
        return is_oob, left_angle, right_angle, 0
    if (new_angle-right_angle)%(2*np.pi)>np.pi:
        is_oob = True
        if seed == -1:
            coeff = np.random.random()
        else:
            coeff = seed


        if (old_angle-right_angle)%(2*np.pi)>1.5*np.pi:
            res_angle = (right_angle+coeff*min_throw_away_angle)%(2*np.pi)
        else:
            res_angle = (left_angle-coeff*min_throw_away_angle)%(2*np.pi)

    return is_oob, left_angle, right_angle, res_angle
    #print()


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_segment_norm_angle(x1, y1, x2, y2):
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

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_collision(vec1, angle, curr_segment):
    x1, y1 = vec1[0], vec1[1]
    x3, y3 = curr_segment[0, 0], curr_segment[0, 1]
    x4, y4 = curr_segment[1, 0], curr_segment[1, 1]
    x2 = x1 + np.sin(angle)
    y2 = y1 + np.cos(angle)
    div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if div == 0:
        # прямая и луч параллельны друг другу
        return False, np.zeros(2), 0.0
    x_cross = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / div
    y_cross = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / div

    if (x_cross - x4) * (x_cross - x3) + (y_cross - y4) * (y_cross - y3) > 0 or (x_cross - x1) * (x2 - x1) + (
            y_cross - y1) * (y2 - y1) <= 0:
        # пересечение вне отрезка
        return False, np.zeros(2), 0.0
    else:
        # пересечение на отрезке
        # print(x3, y3, x4, y4, x_cross, y_cross)
        cross_vec = np.zeros(2)
        cross_vec[0], cross_vec[1] = x_cross, y_cross
        return True, cross_vec, count_segment_norm_angle(x3, y3, x4, y4)


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_vec_mult(delta_x1, delta_y1, delta_x2, delta_y2):
    return delta_x1*delta_y2-delta_x2*delta_y1
