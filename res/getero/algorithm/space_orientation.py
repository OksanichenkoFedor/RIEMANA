from numba import njit
import numpy as np


@njit()
def find_prev_old(curr_x, curr_y, prev_x, prev_y, curr_angle, is_on_horiz):
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
        # print("d")
        curr_att_y = int(curr_y)
        prev_att_y = int(prev_y)
    else:
        # print("dd")
        curr_att_y = int(curr_y) - 1
        prev_att_y = int(prev_y)
        if prev_att_y - curr_att_y > 1:
            curr_att_y += 1

    if (curr_angle <= 1.0 * np.pi) or is_on_horiz:
        # print("ddd")
        curr_att_x = int(curr_x)
        prev_att_x = int(prev_x)
        if is_on_horiz:
            prev_att_x = curr_att_x
    else:
        # print("dddd")
        curr_att_x = int(curr_x) - 1
        prev_att_x = int(prev_x)
        if prev_att_x - curr_att_x > 1:
            curr_att_x += 1
    if np.abs(curr_att_x - prev_att_x) > 1 or np.abs(curr_att_y - prev_att_y) > 1:
        print("find_prev incorr: ", curr_x, curr_y, prev_x, prev_y, curr_angle / np.pi, is_on_horiz)
        print(curr_att_x, curr_att_y, prev_att_x, prev_att_y)
        print("---")
    return curr_att_x, prev_att_x, curr_att_y, prev_att_y


@njit()
def find_next(next_x, next_y, curr_x, curr_y, curr_att_x, curr_att_y):
    if (curr_x is None) and (curr_y is None):
        return int(curr_att_x), int(curr_att_y)
    if int(next_x) - next_x == 0:
        if next_y > curr_att_y + 1:
            next_att_y = curr_att_y + 1
            next_att_x = curr_att_x
        elif next_y < curr_att_y:
            next_att_y = curr_att_y - 1
            next_att_x = curr_att_x
        else:
            next_att_y = curr_att_y
            if next_x - curr_x > 0:
                next_att_x = curr_att_x + 1
            else:
                next_att_x = curr_att_x - 1
    elif int(next_y) - next_y == 0:
        if next_x > curr_att_x + 1:
            next_att_x = curr_att_x + 1
            next_att_y = curr_att_y
        elif next_x < curr_att_x:
            next_att_x = curr_att_x - 1
            next_att_y = curr_att_y
        else:
            next_att_x = curr_att_x
            if next_y - curr_y > 0:
                next_att_y = curr_att_y + 1
            else:
                next_att_y = curr_att_y - 1
    else:
        print("Problem with find_next: ", next_x, next_y, curr_x, curr_y)

    return int(next_att_x), int(next_att_y)


def find_prev1(curr_x, curr_y, prev_x, prev_y, curr_angle, is_on_horiz):
    if (prev_x is None) and (prev_y is None):
        prev_y, prev_x = curr_y, curr_x


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

    return 1.0 * x_coord, 1.0 * y_coord, is_on_horiz


@njit()
def throw_particle_away(is_full_arr, prev_att_x, prev_att_y, curr_x, curr_y):
    add_x, add_y = 0, 0
    if is_full_arr[prev_att_x - 1, prev_att_y] != 1:
        add_x = -1
    elif is_full_arr[prev_att_x, prev_att_y - 1] != 1:
        add_y = -1
    elif is_full_arr[prev_att_x + 1, prev_att_y] != 1:
        add_x = +1
    elif is_full_arr[prev_att_x, prev_att_y + 1] != 1:
        add_y = +1
    else:
        print("Unexpected cage!")

    return prev_att_x + add_x, prev_att_y + add_y, curr_x + add_x, curr_y + add_y
