import numpy as np
from numba import njit
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


@njit()
def give_part_of_border(border_arr, target_x, target_y, num_one_side_points):
    # ищем начало
    X, Y = np.zeros(2 * num_one_side_points + 1), np.zeros(2 * num_one_side_points + 1)
    X[num_one_side_points] = target_x + 0.5
    Y[num_one_side_points] = target_y + 0.5
    start_x, start_y = target_x, target_y
    for i in range(num_one_side_points):
        new_x, new_y = border_arr[start_x, start_y, 1], border_arr[start_x, start_y, 2]
        if new_x != -1 and new_y != -1:
            start_x, start_y = new_x, new_y
        X[num_one_side_points - (i + 1)] = start_x + 0.5
        Y[num_one_side_points - (i + 1)] = start_y + 0.5

    end_x, end_y = target_x, target_y
    for i in range(num_one_side_points):
        new_x, new_y = border_arr[end_x, end_y, 3], border_arr[end_x, end_y, 4]
        if new_x != -1 and new_y != -1:
            end_x, end_y = new_x, new_y
        X[num_one_side_points + (i + 1)] = end_x + 0.5
        Y[num_one_side_points + (i + 1)] = end_y + 0.5

    return X, Y, num_one_side_points


@njit()
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


@njit()
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


@njit()
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


@njit()
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


@njit()
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


@njit()
def give_coefs_line(x, y):
    X = np.ones((x.shape[0], 2))
    X[:, 0] = x
    X[:, 1] = y
    w = np.linalg.pinv(X) @ np.ones((x.shape[0], 1))[:, 0]
    return w


@njit()
def count_norm_angle(border_arr, curr_att_x, curr_att_y, curr_x, curr_y, prev_x, prev_y):
    bX, bY, num = give_part_of_border(border_arr, curr_att_x, curr_att_y, num_one_side_points=2)
    A, B = give_coefs_line(bX, bY)
    n_angle, _, _ = line_approximation(curr_x, curr_y, prev_x, prev_y, A, B, 1)
    return n_angle


# @njit()
def is_collide(curr_x, curr_y, prev_x, prev_y, c_a_x0, c_a_y0, border_layer, curr_angle):
    print("is_collide: ", curr_x, curr_y, prev_x, prev_y, c_a_x0, c_a_y0)
    print(curr_x, curr_y)
    p_a_x, p_a_y = border_layer[c_a_x0, c_a_y0, 1] + 0.5, border_layer[c_a_x0, c_a_y0, 2] + 0.5
    n_a_x, n_a_y = border_layer[c_a_x0, c_a_y0, 3] + 0.5, border_layer[c_a_x0, c_a_y0, 4] + 0.5
    c_a_x = 0.5 + c_a_x0
    c_a_y = 0.5 + c_a_y0

    A_p = (c_a_y - p_a_y)
    B_p = (p_a_x - c_a_x)
    C_p = (c_a_x * (c_a_y - p_a_y) - c_a_y * (c_a_x - p_a_x))
    print("prev line: ", A_p, B_p)
    A_n = (c_a_y - n_a_y)
    B_n = (n_a_x - c_a_x)
    C_n = (c_a_x * (c_a_y - n_a_y) - c_a_y * (c_a_x - n_a_x))
    print("next line: ", A_n, B_n)
    a_p, x_p, y_p = line_approximation(curr_x, curr_y, prev_x, prev_y, A_p, B_p, C_p)
    a_n, x_n, y_n = line_approximation(curr_x, curr_y, prev_x, prev_y, A_n, B_n, C_n)
    collide = False
    if (x_p > c_a_x0 and x_p <= c_a_x0 + 1) and (y_p > c_a_y0 and y_p <= c_a_y0 + 1):
        if (x_p - c_a_x) * (c_a_x - p_a_x) < 0:
            collide = True
        elif (y_p - c_a_y) * (c_a_y - p_a_y) < 0:
            collide = True
    if (x_n > c_a_x0 and x_n <= c_a_x0 + 1) and (y_n > c_a_y0 and y_n <= c_a_y0 + 1):
        if (x_n - c_a_x) * (c_a_x - n_a_x) < 0:
            collide = True
        elif (y_n - c_a_y) * (c_a_y - n_a_y) < 0:
            collide = True
    print(collide)
    rect = Rectangle
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot([p_a_x, c_a_x], [p_a_y, c_a_y], color="g")
    ax.plot(x_p, y_p, ".", color="g")
    ax.plot([n_a_x, c_a_x], [n_a_y, c_a_y], color="b")
    ax.plot(x_n, y_n, ".", color="b")
    ax.arrow(curr_x, curr_y, 0.5*np.sin(curr_angle), 0.5*np.cos(curr_angle), color="k")
    #ax.Rectangle((c_a_x0, c_a_y0), 1, 1, color="b")
    ax.plot([c_a_x0, c_a_x0 + 1, c_a_x0 + 1, c_a_x0, c_a_x0], [c_a_y0, c_a_y0, c_a_y0 + 1, c_a_y0 + 1, c_a_y0], color="r")
    ax.invert_yaxis()
    ax.set_aspect(1)
    plt.show()

    return collide
