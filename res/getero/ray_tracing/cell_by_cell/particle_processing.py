


import numpy as np

from res.getero.ray_tracing.bvh.collision_functions import count_curr_prev_att
from res.getero.ray_tracing.cell_by_cell.collision_functions import check_cell_intersection, particle_on_wall
from res.getero.ray_tracing.utils import check_angle_collision

from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.ray_tracing.cell_by_cell.space_orientation import find_next, give_next_cell

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point
from res.getero.ray_tracing.profile_approximation import count_norm_angle
from res.getero.algorithm.utils import straight_reflection


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                         returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                         params, Si_num, xsize, ysize, R, test, do_half, max_value, num_one_side_points,
                         curr_segment=np.zeros((2, 2))):
    curr_vec = np.zeros(2)
    curr_vec[0] = params[0]
    curr_vec[1] = params[1]
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    prev_att_x = int(params[6])
    prev_att_y = int(params[7])
    curr_att_x, curr_att_y = prev_att_x, prev_att_y
    prev_vec = np.zeros(2)
    prev_vec[0], prev_vec[1] = -10, -10
    unfound = True
    changed_angle = False
    num = 0
    unfound_test = True
    not_max_value = True
    empty_prev = True
    is_inside_cell = False

    if curr_vec[0] - int(curr_vec[0]) != 0 and curr_vec[1] - int(curr_vec[1]) != 0:
        is_inside_cell = True


    while unfound and not_max_value:
        num+=1
        if (num > 10000 and unfound_test):
            if curr_type == 9.0:
                print("Argon in cage!")
            else:
                print("Starange: ", curr_type)
                print([curr_vec[0], curr_vec[1], is_on_horiz, curr_en, curr_angle, curr_type, prev_att_x,
                       prev_att_y])
                unfound_test = False
                #unfound = False
        if is_inside_cell:
            if (curr_att_x!=int(curr_vec[0])) or (curr_att_y!=int(curr_vec[1])):
                print("fff: ", curr_vec ,curr_att_x, curr_att_y)
            if is_full_arr[curr_att_x, curr_att_y] == 0:
                new_vec, prev_att_x, prev_att_y = particle_on_wall(curr_att_x, curr_att_y, curr_vec, curr_angle)
                curr_vec = new_vec.copy()
                if int(curr_vec[0]) - curr_vec[0] == 0:
                    is_on_horiz = 0
                else:
                    is_on_horiz = 1
                changed_angle = True
                is_inside_cell = False
                curr_segment = np.zeros((2,2))
            else:
                is_collide, cross_vec, new_segment = check_cell_intersection(border_layer_arr, curr_att_x, curr_att_y,
                                                                             curr_vec, curr_angle, curr_segment)
                if np.abs(new_segment - curr_segment).sum() == 0 and is_collide:
                    print("coninue: ", cross_vec, curr_angle / np.pi, curr_att_x, curr_att_y)
                else:
                    curr_segment = new_segment
                if is_collide:
                    is_inside_cell = True
                    curr_vec = cross_vec.copy()
                    avg_norm_angle, _, _, _, _, _, _ = count_norm_angle(border_layer_arr, curr_vec, curr_segment,
                                                                        do_half,
                                                                        num_one_side_points=num_one_side_points)
                    tmp_att = count_curr_prev_att(cross_vec, curr_segment, curr_angle, border_layer_arr)
                    tmp_curr_att_x, tmp_curr_att_y, tmp_prev_att_x, tmp_prev_att_y, _ = tmp_att
                    if test:
                        pass
                        arr_x.append(curr_vec[0] - 0.5)
                        arr_y.append(curr_vec[1] - 0.5)

                    if is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == 2.0:
                        new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    elif is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == -1.0:
                        print("Unexpected is_full_arr[curr_att_x, curr_att_y] == -1.0")
                        new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    elif is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == 1.0:
                        curr_type, curr_en, unfound, new_angle = silicon_cycle(counter_arr, is_full_arr,
                                                                               border_layer_arr, returned_particles,
                                                                               curr_angle, avg_norm_angle,
                                                                               tmp_curr_att_x, tmp_curr_att_y,
                                                                               tmp_prev_att_x, tmp_prev_att_y,
                                                                               curr_type, Si_num, curr_en, R,
                                                                               xsize, ysize, test,
                                                                               curr_vec, is_on_horiz, rarr_x, rarr_y,
                                                                               do_half, max_value, num_one_side_points)

                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, curr_segment, curr_vec)
                    curr_angle = new_angle

                else:
                    new_vec, prev_att_x, prev_att_y = particle_on_wall(curr_att_x, curr_att_y, curr_vec, curr_angle)
                    curr_vec = new_vec.copy()
                    if int(curr_vec[0]) - curr_vec[0] == 0:
                        is_on_horiz = 0
                    else:
                        is_on_horiz = 1
                    changed_angle = True
                    is_inside_cell = False
                    curr_segment = np.zeros((2, 2))
        else:
            curr_att_x, curr_att_y = find_next(curr_vec[0], curr_vec[1], prev_vec[0], prev_vec[1], prev_att_x,
                                               prev_att_y, empty_prev)
            empty_prev = False

            if is_full_arr[curr_att_x, curr_att_y] == 0:
                if border_layer_arr[curr_att_x, curr_att_y, 0] != -1 and curr_att_x != xsize - 1:
                    print("Некорректный расчёт профиля! ", border_layer_arr[curr_att_x, curr_att_y, 0], curr_att_x,
                          curr_att_y)
                prev_vec = curr_vec.copy()
                prev_att_x, prev_att_y = curr_att_x, curr_att_y
                curr_vec[0], curr_vec[1], new_is_on_horiz = give_next_cell(prev_vec[0], prev_vec[1], curr_angle,
                                                                           is_on_horiz)
                if test:
                    pass
                    arr_x.append(curr_vec[0] - 0.5)
                    arr_y.append(curr_vec[1] - 0.5)

                is_on_horiz = new_is_on_horiz
            else:
                is_collide, cross_vec, new_segment = check_cell_intersection(border_layer_arr, curr_att_x, curr_att_y,
                                                                             curr_vec, curr_angle, curr_segment)
                if np.abs(new_segment - curr_segment).sum() == 0 and is_collide:
                    print("coninue: ", cross_vec, curr_angle / np.pi, curr_att_x, curr_att_y)
                else:
                    curr_segment = new_segment
                if is_collide:
                    is_inside_cell = True
                    curr_vec = cross_vec.copy()
                    avg_norm_angle, _, _, _, _, _, _ = count_norm_angle(border_layer_arr, curr_vec, curr_segment,
                                                                        do_half,
                                                                        num_one_side_points=num_one_side_points)
                    tmp_att = count_curr_prev_att(cross_vec, curr_segment, curr_angle, border_layer_arr)
                    tmp_curr_att_x, tmp_curr_att_y, tmp_prev_att_x, tmp_prev_att_y, _ = tmp_att
                    if test:
                        pass
                        arr_x.append(curr_vec[0] - 0.5)
                        arr_y.append(curr_vec[1] - 0.5)

                    if is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == 2.0:
                        new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    elif is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == -1.0:
                        print("Unexpected is_full_arr[curr_att_x, curr_att_y] == -1.0")
                        new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    elif is_full_arr[tmp_curr_att_x, tmp_curr_att_y] == 1.0:
                        curr_type, curr_en, unfound, new_angle = silicon_cycle(counter_arr, is_full_arr,
                                                                               border_layer_arr, returned_particles,
                                                                               curr_angle, avg_norm_angle,
                                                                               tmp_curr_att_x, tmp_curr_att_y,
                                                                               tmp_prev_att_x, tmp_prev_att_y,
                                                                               curr_type, Si_num, curr_en, R,
                                                                               xsize, ysize, test,
                                                                               curr_vec, is_on_horiz, rarr_x, rarr_y,
                                                                               do_half, max_value, num_one_side_points)

                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, curr_segment, curr_vec)
                    curr_angle = new_angle
                else:
                    new_vec, prev_att_x, prev_att_y = particle_on_wall(curr_att_x, curr_att_y, curr_vec, curr_angle)
                    curr_vec = new_vec.copy()
                    if int(curr_vec[0]) - curr_vec[0] == 0:
                        is_on_horiz = 0
                    else:
                        is_on_horiz = 1
                    changed_angle = True
                    is_inside_cell = False
                    curr_segment = np.zeros((2, 2))

        curr_angle, prev_att_x, prev_att_y, unfound, changed_angle = check_out(curr_vec, xsize, ysize, do_half,
                                                                               curr_att_x, curr_att_y, prev_att_x,
                                                                               prev_att_y, is_on_horiz, curr_angle,
                                                                               returned_particles, curr_type,
                                                                               unfound, changed_angle)

        if changed_angle:
            # print("changed angle")
            prev_vec[0], prev_vec[1] = -10, -10
            empty_prev = True

            changed_angle = False


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def check_out(curr_vec, xsize, ysize, do_half, curr_att_x, curr_att_y, prev_att_x, prev_att_y, is_on_horiz, curr_angle,
              returned_particles, curr_type, unfound, changed_angle):
    new_angle = curr_angle
    new_prev_att_x, new_prev_att_y = prev_att_x, prev_att_y
    if curr_vec[0] >= xsize:
        if do_half:
            new_prev_att_x, new_prev_att_y = curr_att_x, curr_att_y
            if is_on_horiz != 0:
                print("Incorrect is_on_horiz: ", is_on_horiz)
            new_angle = straight_reflection(curr_angle, np.pi * 0.5)
            changed_angle = True
        else:
            unfound = False
            returned_particles[int(curr_type)] += 1
    if curr_vec[0] < 0 or (curr_vec[1] >= ysize or curr_vec[1] < 0):
        unfound = False
        returned_particles[int(curr_type)] += 1
    elif int(curr_vec[1]) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
        unfound = False
        returned_particles[int(curr_type)] += 1

    return new_angle, new_prev_att_x, new_prev_att_y, unfound, changed_angle


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def silicon_cycle(counter_arr, is_full_arr, border_layer_arr, returned_particles, curr_angle, avg_norm_angle,
                  curr_att_x, curr_att_y, prev_att_x, prev_att_y, curr_type, Si_num, curr_en, R, xsize, ysize, test,
                  curr_vec, is_on_horiz, rarr_x, rarr_y, do_half, max_value, num_one_side_points):
    angles = np.zeros(2)
    angles[0], angles[1] = curr_angle, avg_norm_angle

    point_vector = np.zeros((2, 2))
    point_vector[0, 0], point_vector[0, 1] = curr_att_x, curr_att_y
    point_vector[1, 0], point_vector[1, 1] = prev_att_x, prev_att_y

    if counter_arr[:, curr_att_x, curr_att_y].sum() == 0.0:
        print("---")
        print("Пустая не пустая!!!")
        print(curr_att_x, curr_att_y)
        print("---")

    new_type, new_en, flags, redepo_params, new_angle = silicon_reaction(curr_type, counter_arr,
                                                                         is_full_arr, point_vector,
                                                                         Si_num, angles, curr_en, R)

    if new_type in [7, 8, 9] and (not test):
        # родились бесполезные частицы рассматриваем их только когда тест
        unfound = False
        returned_particles[int(curr_type)] += 1

    if flags[2] == 1.0:
        # удаление
        # 0 - внутри
        # 1 - граница
        # -1 - снаружи
        # 2 - граница, но пустые точки
        delete_point(border_layer_arr, is_full_arr, curr_att_x, curr_att_y)
        print("Delete: ", curr_att_x, curr_att_y)
        if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
            print("Удаление не произведено!")
        if is_full_arr[curr_att_x, curr_att_y]:
            print("Непредсказуемое удаление!!!")

    if flags[3] == 1.0:
        # восстановление частицы
        print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
        create_point(border_layer_arr, is_full_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)

    if flags[1] == 1.0:
        redepo_params[0] = curr_vec[0]
        redepo_params[1] = curr_vec[1]
        redepo_params[2] = is_on_horiz
        redepo_params[6] = curr_att_x
        redepo_params[7] = curr_att_y
        process_one_particle(counter_arr, is_full_arr, border_layer_arr, returned_particles,
                             rarr_x, rarr_y, rarr_x, rarr_y, redepo_params, Si_num, xsize, ysize, R,
                             test, do_half, max_value, num_one_side_points)
    if flags[0] == 1.0:
        unfound = False
    return new_type, new_en, unfound, new_angle


