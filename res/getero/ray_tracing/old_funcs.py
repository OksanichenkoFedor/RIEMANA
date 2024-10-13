import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.ray_tracing.utils import count_angle


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def parabola_approximation(curr_x, curr_y, prev_x, prev_y, a, b, c, tp):
    if tp:
        curr_x, curr_y = curr_y, curr_x
        prev_x, prev_y = prev_y, prev_x

    alpha = (curr_y - prev_y) / (curr_x - prev_x)
    beta = (curr_x * prev_y - curr_y * prev_x) / (curr_x - prev_x)

    det = (alpha - b) ** 2 - 4 * a * (c - beta)
    x_a = ((alpha - b) + np.sqrt(det)) / (2 * a)
    y_a = alpha * x_a + beta

    x_b = ((alpha - b) - np.sqrt(det)) / (2 * a)
    y_b = alpha * x_b + beta
    if (x_a - curr_x) * (curr_x - prev_x) > 0:
        x_1, y_1 = x_a, y_a
    else:
        x_1, y_1 = x_b, y_b
    gamma_1 = [-1 * (2 * a * x_1 + b), 1]
    gamma_2 = [(2 * a * x_1 + b), -1]
    if gamma_1[0] * (curr_x - prev_x) + gamma_1[1] * (curr_y - prev_y) < 0:
        gamma = gamma_1
    else:
        gamma = gamma_2

    if tp:
        return count_angle(gamma[0], gamma[1]), y_1, x_1
    else:
        return count_angle(gamma[1], gamma[0]), x_1, y_1


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def second_curve_approximation(curr_x, curr_y, prev_x, prev_y, A, B, C, D, E):
    alpha = (curr_y - prev_y) / (curr_x - prev_x)
    beta = (curr_x * prev_y - curr_y * prev_x) / (curr_x - prev_x)

    a = A + alpha * B + alpha * alpha * C
    b = B * beta + 2 * C * alpha * beta + D + E * alpha
    c = C * beta * beta + E * beta - 1
    x_a = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x_b = (-b + np.sqrt(b ** 2 + 4 * a * c)) / (2 * a)

    hi_a = (x_a - curr_x) * (curr_x - prev_x)
    hi_b = (x_b - curr_x) * (curr_x - prev_x)

    if hi_a > 0 and hi_b < 0:
        print("a")
        x_1 = x_a
    elif hi_a < 0 and hi_b > 0:
        print("b")
        x_1 = x_b
    elif hi_a > 0 and hi_b > 0:
        if hi_a < hi_b:
            print("c")
            x_1 = x_a
        else:
            print("d")
            x_1 = x_b
    y_1 = alpha * x_1 + beta

    k = (-B * y_1 - D - 2 * A * x_1) / (B * x_1 + 2 * C * y_1 + E)
    gamma_1 = [-k, 1]
    gamma_2 = [k, -1]
    if gamma_1[0] * (curr_x - prev_x) + gamma_1[1] * (curr_y - prev_y) < 0:
        gamma = gamma_1
    else:
        gamma = gamma_2

    return count_angle(gamma[1], gamma[0]), x_1, y_1

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def line_approximation(curr_x, curr_y, prev_x, prev_y, A, B, C):
    alpha = (curr_y - prev_y)
    beta = (curr_x * prev_y - curr_y * prev_x)
    kappa = (curr_x - prev_x)

    x_1 = (C * kappa - beta * B) / (A * kappa + alpha * B)
    if kappa == 0:
        y_1 = (C - A * x_1) / B
    else:
        y_1 = (alpha * x_1 + beta) / kappa

    gamma_1 = [A, B]
    gamma_2 = [-A, -B]
    if gamma_1[0] * (curr_x - prev_x) + gamma_1[1] * (curr_y - prev_y) < 0:
        gamma = gamma_1
    else:
        gamma = gamma_2

    return count_angle(gamma[1], gamma[0]), x_1, y_1
