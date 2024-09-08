from numba import njit
import numpy as np

from res.getero.algorithm.dynamic_profile import give_start


@njit()
def simple_count_collision_point(border_layer_arr, x_ray, y_ray, curr_angle):
    found = False
    x_cross, y_cross = 0, 0
    dist2 = 0
    norm_angle = 0
    x_start, y_start = give_start(border_layer_arr)
    x_end, y_end = border_layer_arr[x_start, y_start, 3:]
    unfound_end = True
    while unfound_end:
        if (border_layer_arr[x_end, y_end, 3] == -1) and (border_layer_arr[x_end, y_end, 4] == -1):
            unfound_end = False
        is_cross, c_x, c_y, c_na = check_collision(x_ray, y_ray, curr_angle, x_start + 0.5, y_start + 0.5, x_end + 0.5,
                                                   y_end + 0.5)
        x_start, y_start = x_end, y_end
        x_end, y_end = border_layer_arr[x_start, y_start, 3:]
        if is_cross:
            if found:
                c_d = (c_x - x_ray) * (c_x - x_ray) + (c_y - y_ray) * (c_y - y_ray)
                if dist2 > c_d > 10 ** (-5):
                    dist2 = c_d
                    norm_angle = c_na
                    x_cross, y_cross = c_x, c_y
            else:
                c_d = (c_x - x_ray) * (c_x - x_ray) + (c_y - y_ray) * (c_y - y_ray)
                if c_d > 10 ** (-5):
                    found = True
                    x_cross, y_cross = c_x, c_y
                    dist2 = (x_cross - x_ray) * (x_cross - x_ray) + (y_cross - y_ray) * (y_cross - y_ray)
                    norm_angle = c_na

    return found, x_cross, y_cross, norm_angle


@njit()
def check_collision(x1, y1, angle, x3, y3, x4, y4):
    x2 = x1 + np.sin(angle)
    y2 = y1 + np.cos(angle)
    div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if div == 0:
        # прямая и луч параллельны друг другу
        return False, 0.0, 0.0, 0.0
    x_cross = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / div
    y_cross = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / div

    if (x_cross - x4) * (x_cross - x3) + (y_cross - y4) * (y_cross - y3) > 0 or (x_cross - x1) * (x2 - x1) + (
            y_cross - y1) * (y2 - y1) <= 0:
        # пересечение вне отрезка
        return False, 0.0, 0.0, 0.0
    else:
        # пересечение на отрезке
        # print(x3, y3, x4, y4, x_cross, y_cross)
        return True, x_cross, y_cross, count_norm_angle(x3, y3, x4, y4)


@njit()
def count_norm_angle(x1, y1, x2, y2):
    # Пустота всегда слева от лини поэтому мы всегда явно можем определить угол от нормали.
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
