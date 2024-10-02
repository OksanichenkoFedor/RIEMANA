import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.algorithm.space_orientation import find_next, give_next_cell, throw_particle_away

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.mask_reactions import mask_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point
from res.getero.algorithm.ray_tracing.profile_approximation import count_simple_norm_angle
from res.getero.algorithm.utils import straight_reflection


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                         returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                         params, Si_num, xsize, ysize, R, test, do_half, max_value, num_one_side_points):
    curr_x = params[0]
    curr_y = params[1]
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    prev_att_x = int(params[6])
    # if int(curr_y) == params[7] and (curr_angle>0.5*np.pi and curr_angle<1.5*np.pi):
    #    prev_att_y = int(params[7])-1
    # else:
    #    prev_att_y = int(params[7])
    prev_att_y = int(params[7])
    prev_y, prev_x = None, None
    unfound = True
    changed_angle = False
    num = 0
    unfound_test = True
    not_max_value = True
    #is_collide, x_c, y_c = simple_count_collision_point(border_layer_arr, curr_x, curr_y, curr_angle)
    while unfound and not_max_value:

        if max_value != -1.0:
            if num > max_value:
                not_max_value = False
        num += 1
        curr_att_x, curr_att_y = find_next(curr_x, curr_y, prev_x, prev_y, prev_att_x, prev_att_y)
        # print(curr_att_x, curr_att_y, curr_x, curr_y, is_on_horiz)
        if (curr_att_x == prev_att_x and curr_att_y == prev_att_y) and (not (prev_y is None)):
            pass
            print("Ахтунг!!!!")
            print(curr_x, curr_y, prev_x, prev_y)
            print(curr_att_x, prev_att_x, curr_att_y, prev_att_y)
            print(curr_angle, curr_angle / np.pi)
            print(is_full_arr[curr_att_x, curr_att_y])
        if is_full_arr[curr_att_x, curr_att_y] == 1.0:
            if (num > 10000 and unfound_test):
                if curr_type == 9.0:
                    print("Argon in cage!")
                else:
                    print("Starange: ", curr_type)
                    print([curr_x, curr_y, is_on_horiz, curr_en, curr_angle, curr_type, prev_att_x, prev_att_y])
                    unfound_test = False
            curr_counter = counter_arr[:, curr_att_x, curr_att_y]
            prev_counter = counter_arr[:, prev_att_x, prev_att_y]
            curr_farr = is_full_arr[curr_att_x, curr_att_y]
            prev_farr = is_full_arr[prev_att_x, prev_att_y]
            if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] == 0:
                print("---")
                print("Пустая не пустая!!!")
                print(curr_att_x, curr_att_y)
                print("---")
            n_angle = count_simple_norm_angle(curr_angle, is_on_horiz)
            new_type, new_curr_counter, new_prev_counter, new_curr_farr, new_prev_farr, is_react, new_angle, \
            new_en, is_redepo, redepo_params = silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr,
                                                                prev_farr, Si_num, n_angle, curr_angle, curr_en,
                                                                R)
            if curr_type in [7, 8, 9] and (not test):
                # родились бесполезные частицы рассматриваем их только когда тест
                unfound = False
                returned_particles[int(curr_type)] += 1
            if new_curr_farr != curr_farr:
                # удаление
                # 0 - внутри
                # 1 - граница
                # -1 - снаружи

                delete_point(border_layer_arr, curr_att_x, curr_att_y)
                #print("Delete: ", curr_att_x, curr_att_y)
                if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
                    print("Удаление не произведено!")
                if new_curr_farr:
                    print("Непредсказуемое удаление!!!")

            if new_prev_farr != prev_farr:
                # восстановление частицы
                print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
                create_point(border_layer_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)
            counter_arr[:, curr_att_x, curr_att_y] = new_curr_counter
            counter_arr[:, prev_att_x, prev_att_y] = new_prev_counter
            is_full_arr[curr_att_x, curr_att_y] = new_curr_farr
            is_full_arr[prev_att_x, prev_att_y] = new_prev_farr
            curr_angle = new_angle
            curr_type = new_type
            curr_en = new_en

            if is_redepo:
                redepo_params[0] = curr_x
                redepo_params[1] = curr_y
                redepo_params[2] = is_on_horiz
                redepo_params[6] = prev_att_x
                redepo_params[7] = prev_att_y
                process_one_particle(counter_arr, is_full_arr, border_layer_arr, returned_particles,
                                     rarr_x, rarr_y, rarr_x, rarr_y, redepo_params, Si_num, xsize, ysize, R, test,
                                     do_half, max_value, num_one_side_points)
                if is_full_arr[prev_att_x, prev_att_y] == 1:
                    print("Ловушка джокера")
                    prev_att_x, prev_att_y, curr_x, curr_y = throw_particle_away(is_full_arr, prev_att_x, prev_att_y,
                                                                                 curr_x, curr_y)

            if is_react:
                unfound = False
            else:
                changed_angle = True


        elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
            # Маска
            curr_angle = mask_reaction(is_on_horiz, curr_angle)
            changed_angle = True
        else:
            if border_layer_arr[curr_att_x, curr_att_y, 0] != -1 and curr_att_x!=xsize-1:
                print("Некорректный расчёт профиля! ", border_layer_arr[curr_att_x, curr_att_y, 0], curr_att_x, curr_att_y)
            prev_x = curr_x
            prev_y = curr_y
            prev_att_x, prev_att_y = curr_att_x, curr_att_y

            curr_x, curr_y, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)

            if test:
                pass
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)

            is_on_horiz = new_is_on_horiz
            if curr_x >= xsize:
                if do_half:
                    if is_on_horiz!=0:
                        print("Incorrect is_on_horiz: ", is_on_horiz)
                    curr_angle = straight_reflection(curr_angle, np.pi*0.5)
                    changed_angle = True
                else:
                    unfound = False
                    returned_particles[int(curr_type)] += 1
            if curr_x < 0 or (curr_y >= ysize or curr_y < 0):
                unfound = False
                returned_particles[int(curr_type)] += 1
            elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                unfound = False
                returned_particles[int(curr_type)] += 1

        if changed_angle:
            prev_x, prev_y = None, None

            changed_angle = False
