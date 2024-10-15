import numpy as np

from res.getero.ray_tracing.utils import check_collision
from res.utils.config import do_njit, cache, parallel
from res.utils.wrapper import clever_njit

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_cell_intersection(border_arr, curr_att_x, curr_att_y, curr_vec, curr_angle, start_segment=None):
    if border_arr[curr_att_x, curr_att_y, 0] == -1:
        prev_x, prev_y = border_arr[curr_att_x, curr_att_y, 1] + 0.5, border_arr[curr_att_x, curr_att_y, 2] + 0.5
        next_x, next_y = border_arr[curr_att_x, curr_att_y, 3] + 0.5, border_arr[curr_att_x, curr_att_y, 4] + 0.5
        segment = np.zeros((2, 2))
        segment[0, 0], segment[0, 1] = prev_x, prev_y
        segment[1, 0], segment[1, 1] = next_x, next_y
        collide, cross_vec, norm_angle = check_collision(curr_vec, curr_angle, segment)
        if not collide:
            return False, np.zeros(2), np.zeros((2, 2))

    else:
        curr_x, curr_y = curr_att_x + 0.5, curr_att_y + 0.5

        if border_arr[curr_att_x, curr_att_y, 1] == -1 and border_arr[curr_att_x, curr_att_y, 2] == -1:
            prev_x, prev_y = curr_att_x + 0.0, curr_att_y + 0.5
        else:
            prev_x, prev_y = border_arr[curr_att_x, curr_att_y, 1] + 0.5, border_arr[curr_att_x, curr_att_y, 2] + 0.5

        if border_arr[curr_att_x, curr_att_y, 3] == -1 and border_arr[curr_att_x, curr_att_y, 4] == -1:
            next_x, next_y = curr_att_x + 1.0, curr_att_y + 0.5
        else:
            next_x, next_y = border_arr[curr_att_x, curr_att_y, 3] + 0.5, border_arr[curr_att_x, curr_att_y, 4] + 0.5

        left_segment = np.zeros((2, 2))
        left_segment[0, 0], left_segment[0, 1] = prev_x, prev_y
        left_segment[1, 0], left_segment[1, 1] = curr_x, curr_y

        right_segment = np.zeros((2, 2))
        right_segment[0, 0], right_segment[0, 1] = curr_x, curr_y
        right_segment[1, 0], right_segment[1, 1] = next_x, next_y

        segment = np.zeros((2, 2))
        cross_vec = np.zeros(2)

        left_collide, left_cross_vec, left_norm_angle = check_collision(curr_vec, curr_angle, left_segment)
        right_collide, right_cross_vec, right_norm_angle = check_collision(curr_vec, curr_angle, right_segment)

        if start_segment is None:
            pass
        else:
            left_collide = np.abs(start_segment - left_segment).sum() != 0 and left_collide
            right_collide = np.abs(start_segment - right_segment).sum() != 0 and right_collide

        if left_collide and right_collide:
            if np.pow(curr_vec - left_cross_vec, 2).sum() < np.pow(curr_vec - right_cross_vec, 2).sum():
                cross_vec = left_cross_vec
                segment = left_segment
            else:
                cross_vec = right_cross_vec
                segment = right_segment
        elif (not left_collide) and (not right_collide):
            return False, np.zeros(2), np.zeros((2, 2))
        elif left_collide:
            cross_vec = left_cross_vec
            segment = left_segment
        elif right_collide:
            cross_vec = right_cross_vec
            segment = right_segment
        else:
            print("Strange happens cell_by_cell/collision_functions")
            return False, np.zeros(2), np.zeros((2, 2))

    if (curr_att_x <= cross_vec[0] < curr_att_x + 1) and (curr_att_y <= cross_vec[1] < curr_att_y + 1):
        return True, cross_vec, segment
    else:
        return False, np.zeros(2), np.zeros((2, 2))


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def particle_on_wall(curr_att_x, curr_att_y, curr_vec, curr_angle):
    first_segment, second_segment = np.zeros((2, 2)), np.zeros((2, 2))
    if curr_angle<np.pi*0.5:
        #bottom and right
        first_segment[0, 0], first_segment[0, 1] = curr_att_x, curr_att_y + 1
        first_segment[1, 0], first_segment[1, 1] = curr_att_x + 1, curr_att_y + 1
        second_segment[0, 0], second_segment[0, 1] = curr_att_x + 1, curr_att_y + 1
        second_segment[1, 0], second_segment[1, 1] = curr_att_x + 1, curr_att_y
        first_delta_x, first_delta_y = 0, 1
        second_delta_x, second_delta_y = 1, 0
    elif curr_angle<np.pi:
        #right and up
        first_segment[0, 0], first_segment[0, 1] = curr_att_x + 1, curr_att_y + 1
        first_segment[1, 0], first_segment[1, 1] = curr_att_x + 1, curr_att_y
        second_segment[0, 0], second_segment[0, 1] = curr_att_x + 1, curr_att_y
        second_segment[1, 0], second_segment[1, 1] = curr_att_x, curr_att_y
        first_delta_x, first_delta_y = 1, 0
        second_delta_x, second_delta_y = 0, -1
    elif curr_angle<np.pi*1.5:
        #up and left
        first_segment[0, 0], first_segment[0, 1] = curr_att_x + 1, curr_att_y
        first_segment[1, 0], first_segment[1, 1] = curr_att_x, curr_att_y
        second_segment[0, 0], second_segment[0, 1] = curr_att_x, curr_att_y
        second_segment[1, 0], second_segment[1, 1] = curr_att_x, curr_att_y + 1
        first_delta_x, first_delta_y = 0, -1
        second_delta_x, second_delta_y = -1, 0
    else:
        #left and bottom
        first_segment[0, 0], first_segment[0, 1] = curr_att_x, curr_att_y
        first_segment[1, 0], first_segment[1, 1] = curr_att_x, curr_att_y + 1
        second_segment[0, 0], second_segment[0, 1] = curr_att_x, curr_att_y + 1
        second_segment[1, 0], second_segment[1, 1] = curr_att_x + 1, curr_att_y + 1
        first_delta_x, first_delta_y = -1, 0
        second_delta_x, second_delta_y = 0, 1

    first_collide, first_cross_vec, first_norm_angle = check_collision(curr_vec, curr_angle, first_segment)
    second_collide, second_cross_vec, second_norm_angle = check_collision(curr_vec, curr_angle, second_segment)

    if first_collide and second_collide:
        #print("Both intersect  -> incorrect cell_by_cell/collision_functions particle_on_wall")
        return first_cross_vec, curr_att_x + first_delta_x, curr_att_y + first_delta_y
    elif (not first_collide) and (not second_collide):
        print("None intersect -> incorrect cell_by_cell/collision_functions particle_on_wall")
        return np.zeros(2), 0, 0
    elif first_collide:
        return first_cross_vec, curr_att_x + first_delta_x, curr_att_y + first_delta_y
    elif second_collide:
        return second_cross_vec, curr_att_x + second_delta_x, curr_att_y + second_delta_y
    else:
        print("Strange happens cell_by_cell/collision_functions particle_on_wall")
        return np.zeros(2), 0, 0

