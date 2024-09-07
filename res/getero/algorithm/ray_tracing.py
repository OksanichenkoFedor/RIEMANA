from numba import njit
import numpy as np

from res.getero.algorithm.dynamic_profile import give_start


@njit()
def simple_count_collision_point(border_layer_arr, x_ray, y_ray, curr_angle):
    found = False
    x_cross, y_cross = 0, 0
    dist2 = 0
    x_start, y_start = give_start(border_layer_arr)
    x_end, y_end = border_layer_arr[x_start, y_start, 3:]
    while (border_layer_arr[x_end, y_end, 3] != -1) or (border_layer_arr[x_end, y_end, 4] != -1):
        is_cross, c_x, c_y = check_collision(x_ray, y_ray, curr_angle, x_start, y_start, x_end, y_end)
        x_start, y_start = x_end, y_end
        x_end, y_end = border_layer_arr[x_start, y_start, 3:]
        if is_cross:
            if found:
                found = True
                x_cross, y_cross = c_x, c_y
                dist2 = (x_cross - x_ray) * (x_cross - x_ray) + (y_cross - y_ray) * (y_cross - y_ray)
            else:
                c_d = (c_x - x_ray) * (c_x - x_ray) + (c_y - y_ray) * (c_y - y_ray)
                if c_d < dist2:
                    dist2 = c_d
                    x_cross, y_cross = c_x, c_y
    return found, x_cross, y_cross


@njit()
def check_collision(x1, y1, angle, x3, y3, x4, y4):
    x2 = x1 + np.sin(angle)
    y2 = y1 + np.cos(angle)
    div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if div == 0:
        # прямая и луч параллельны друг другу
        return False, 0.0, 0.0
    x_cross = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / div
    y_cross = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / div

    if (x_cross - x4) * (x_cross - x3) > 0:
        # пересечение вне отрезка
        return False, 0, 0
    else:
        # пересечение на отрезке
        return True, x_cross, y_cross
