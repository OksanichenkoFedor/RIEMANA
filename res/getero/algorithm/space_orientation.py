from numba import njit
import numpy as np

@njit()
def find_prev(curr_x, curr_y, prev_x, prev_y, curr_angle, is_on_horiz):
    """
    Реализует определение предыдущего чанка для корректного наращивания и отражения
    :param curr_x:
    :param curr_y:
    :param prev_x:
    :param prev_y:
    :param curr_angle:
    :param is_on_horiz:
    :return:
    """
    if (prev_x is None) and (prev_y is None):
        prev_y, prev_x = curr_y, curr_x
    if (curr_angle > 1.5 * np.pi or curr_angle < 0.5 * np.pi) or (not is_on_horiz):
        curr_att_y = int(curr_y)
        prev_att_y = int(prev_y)
    else:
        curr_att_y = int(curr_y) - 1
        prev_att_y = int(prev_y) - 1

    if (curr_angle <= 1.0 * np.pi) or is_on_horiz:
        curr_att_x = int(curr_x)
        prev_att_x = int(prev_x)
        if is_on_horiz:
            prev_att_x = curr_att_x
    else:
        curr_att_x = int(curr_x) - 1
        prev_att_x = int(prev_x)
    return curr_att_x, prev_att_x, curr_att_y, prev_att_y

@njit()
def give_next_cell_compl(x_coord, y_coord, angle, is_on_horiz):
    if angle > 1.5 * np.pi or angle < 0.5 * np.pi:
        if angle <= 1.0 * np.pi:
            # летим вправо-вниз
            if is_on_horiz:
                delta_x = np.tan(angle) + x_coord - int(x_coord)
                if delta_x > 1.0:
                    # правая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = 1 + int(x_coord)
                else:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord += np.tan(angle)
                    y_coord += 1
            else:
                delta_y = 1.0 / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = 1 + int(y_coord)
                else:
                    # правая грань
                    is_on_horiz = 0
                    y_coord += 1.0 / np.tan(angle)
                    x_coord += 1
        else:
            # летим влево-вниз
            if is_on_horiz:
                delta_x = np.tan(angle) + x_coord - int(x_coord)
                if delta_x < 0:
                    # левая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = int(x_coord)
                else:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord += np.tan(angle)
                    y_coord += 1
            else:
                delta_y = (-1.0) / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # нижняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = 1 + int(y_coord)
                else:
                    # левая грань
                    is_on_horiz = 0
                    y_coord -= 1.0 / np.tan(angle)
                    x_coord -= 1
    else:
        if angle <= 1.0 * np.pi:
            # летим вправо-вверх
            if is_on_horiz:
                delta_x = (-1.0) * np.tan(angle) + x_coord - int(x_coord)
                if delta_x > 1.0:
                    print("Err? ", x_coord)
                    # правая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = 1 + int(x_coord)
                else:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord -= np.tan(angle)
                    y_coord -= 1
            else:
                delta_y = 1.0 / np.tan(angle) + y_coord - int(y_coord)
                if delta_y > 1.0:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (int(y_coord) - y_coord) / np.tan(angle)
                    y_coord = int(y_coord)
                else:
                    # правая грань
                    is_on_horiz = 0
                    y_coord += 1.0 / np.tan(angle)
                    x_coord += 1
        else:
            # летим влево-вверх
            if is_on_horiz:
                delta_x = (-1.0) * np.tan(angle) + x_coord - int(x_coord)
                if delta_x < 0:
                    # левая грань
                    is_on_horiz = 0
                    y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
                    x_coord = int(x_coord)
                else:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord -= np.tan(angle)
                    y_coord -= 1
            else:
                delta_y = (-1.0) / np.tan(angle) + y_coord - int(y_coord)
                if delta_y < 0.0:
                    # верхняя грань
                    is_on_horiz = 1
                    x_coord = x_coord + (int(y_coord) - y_coord) * np.tan(angle)
                    y_coord = int(y_coord)
                else:
                    # левая грань
                    is_on_horiz = 0
                    y_coord -= 1.0 / np.tan(angle)
                    x_coord -= 1

    return 1.0 * x_coord, 1.0 * y_coord, angle, is_on_horiz


@njit()
def give_next_cell(x_coord, y_coord, angle, is_on_horiz):
    if angle > 1.5 * np.pi or angle < 0.5 * np.pi:
        x_mult = 1.0
    else:
        x_mult = -1.0
    if angle <= 1.0 * np.pi:
        y_mult = 1.0
    else:
        y_mult = -1.0

    if is_on_horiz:
        delta_x = x_mult * np.tan(angle) + x_coord - int(x_coord)
        if delta_x > 1.0:
            is_on_horiz = 0
            y_coord = y_coord + (1 + int(x_coord) - x_coord) / np.tan(angle)
            x_coord = 1 + int(x_coord)
        elif delta_x < 0:
            # левая грань
            is_on_horiz = 0
            y_coord = y_coord + (int(x_coord) - x_coord) / np.tan(angle)
            x_coord = int(x_coord)
        else:
            is_on_horiz = 1
            x_coord += x_mult * np.tan(angle)
            y_coord += x_mult * 1
    else:
        delta_y = y_mult / np.tan(angle) + y_coord - int(y_coord)
        if delta_y > 1.0:
            is_on_horiz = 1
            x_coord = x_coord + (1 + int(y_coord) - y_coord) * np.tan(angle)
            y_coord = 1 + int(y_coord)
        elif delta_y < 0.0:
            is_on_horiz = 1
            x_coord = x_coord + (int(y_coord) - y_coord) * np.tan(angle)
            y_coord = int(y_coord)
        else:
            is_on_horiz = 0
            y_coord += y_mult * 1.0 / np.tan(angle)
            x_coord += y_mult * 1

    return 1.0 * x_coord, 1.0 * y_coord, angle, is_on_horiz
