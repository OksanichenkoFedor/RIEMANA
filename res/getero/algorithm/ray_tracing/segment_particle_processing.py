import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel
import numba as nb

from res.getero.algorithm.utils import straight_reflection
from res.getero.algorithm.ray_tracing.bvh import bvh_count_collision_point, build_BVH
from res.getero.algorithm.ray_tracing.line_search import simple_count_collision_point
from res.getero.algorithm.ray_tracing.collision_functions import count_curr_prev_att
from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point, find_close_void
from res.getero.algorithm.space_orientation import throw_particle_away

@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr, NodeList,
                         returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                         params, Si_num, xsize, ysize, R, test, do_half, max_value, type):
    curr_vec = np.zeros(2)
    curr_vec[0] = params[0]
    curr_vec[1] = params[1]
    start_segment = np.ones((2,2))*(-1.0)
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    unfound = True
    not_max_value = True
    if test:
        pass
        arr_x.append(curr_vec[0] - 0.5)
        arr_y.append(curr_vec[1] - 0.5)
    while unfound and not_max_value:
        #print("start bvh")
        if type=="bvh":
            is_collide, coll_vec, norm_angle, start_segment = bvh_count_collision_point(NodeList, curr_vec, curr_angle, start_segment)
        else:
            is_collide, coll_vec, norm_angle, start_segment = simple_count_collision_point(border_layer_arr, curr_vec,
                                                                         curr_angle, start_segment)
        st_x, st_y = int(start_segment[0, 0] - 0.5), int(start_segment[0, 1] - 0.5)
        en_x, en_y = int(start_segment[1, 0] - 0.5), int(start_segment[1, 1] - 0.5)
        if is_full_arr[st_x, st_y]==0 or is_full_arr[en_x, en_y]==0:
            pass
            #print("Некорректная постройка границы:", is_full_arr[st_x, st_y], is_full_arr[en_x, en_y])
        #print("end bvh, start collision processing")
        if is_collide:
            if test:
                pass
                arr_x.append(coll_vec[0] - 0.5)
                arr_y.append(coll_vec[1] - 0.5)

            curr_att_x, curr_att_y, prev_att_x, prev_att_y, _ = count_curr_prev_att(coll_vec, start_segment, curr_angle,
                                                                                 border_layer_arr)
            if is_full_arr[prev_att_x, prev_att_y]==1:
                print("Граница на пустоте: ", prev_att_x, prev_att_y)
            if is_full_arr[curr_att_x, curr_att_y] == 1.0:

                curr_counter = counter_arr[:, curr_att_x, curr_att_y]
                prev_counter = counter_arr[:, prev_att_x, prev_att_y]
                curr_farr = is_full_arr[curr_att_x, curr_att_y]
                prev_farr = is_full_arr[prev_att_x, prev_att_y]
                if curr_counter[0] + curr_counter[1] + curr_counter[2] + curr_counter[3] == 0:
                    print("---")
                    print("Пустая не пустая!!!")
                    print(curr_att_x, curr_att_y)
                    print("---")
                #print("start silicon_reactions")
                new_type, new_curr_counter, new_prev_counter, new_curr_farr, new_prev_farr, is_react, new_angle, \
                    new_en, is_redepo, redepo_params = silicon_reaction(curr_type, curr_counter, prev_counter,
                                                                        curr_farr,
                                                                        prev_farr, Si_num, norm_angle, curr_angle, curr_en,
                                                                        R)
                #print("end silicon_reactions")
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
                    if type == "bvh":
                        NodeList = build_BVH(border_layer_arr)
                    #print("Delete: ", curr_att_x, curr_att_y)
                    if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
                        print("Удаление не произведено!")
                    if new_curr_farr:
                        print("Непредсказуемое удаление!!!")

                if new_prev_farr != prev_farr:
                    # восстановление частицы
                    print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
                    create_point(border_layer_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)
                    if type=="bvh":
                        NodeList = build_BVH(border_layer_arr)
                    new_x, new_y = find_close_void(border_layer_arr, prev_att_x, prev_att_y)
                    coll_vec[0], coll_vec[1] = (prev_att_x+0.5+0.1*(new_x-prev_att_x),
                                                prev_att_y+0.5+0.1*(new_y-prev_att_y))
                    start_segment[0, 0], start_segment[0, 1] = -1, -1
                    start_segment[1, 0], start_segment[1, 1] = -1, -1
                counter_arr[:, curr_att_x, curr_att_y] = new_curr_counter
                counter_arr[:, prev_att_x, prev_att_y] = new_prev_counter
                is_full_arr[curr_att_x, curr_att_y] = new_curr_farr
                is_full_arr[prev_att_x, prev_att_y] = new_prev_farr
                curr_angle = new_angle
                curr_type = new_type
                curr_en = new_en

                if is_redepo:
                    #print("is_redepo!!!")
                    redepo_params[0] = coll_vec[0]
                    redepo_params[1] = coll_vec[1]
                    redepo_params[2] = 0#is_on_horiz
                    redepo_params[6] = prev_att_x
                    redepo_params[7] = prev_att_y
                    NodeList = process_one_particle(counter_arr, is_full_arr, border_layer_arr, NodeList,
                                                    returned_particles, rarr_x, rarr_y, rarr_x, rarr_y, redepo_params,
                                                    Si_num, xsize, ysize, R, test, do_half, max_value, type)
                    if is_full_arr[prev_att_x, prev_att_y] == 1:
                        pass
                        print("Ловушка джокера")
                        #prev_att_x, prev_att_y, curr_x, curr_y = throw_particle_away(is_full_arr, prev_att_x,
                        #                                                             prev_att_y,
                        #                                                             curr_x, curr_y)

                if is_react:
                    unfound = False
            elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
                # Маска
                curr_angle = straight_reflection(curr_angle, norm_angle)
            else:
                print("Мы ударились о пустоту! ",coll_vec,start_segment, curr_att_x, curr_att_y, is_full_arr[curr_att_x, curr_att_y])
                curr_angle = straight_reflection(curr_angle, norm_angle)
            curr_vec = coll_vec
        else:
            unfound = False
            if test:
                pass
                arr_x.append(curr_vec[0] - 0.5 + np.sin(curr_angle)*5)
                arr_y.append(curr_vec[1] - 0.5 + np.cos(curr_angle)*5)
        #print("end collision processing")
        return NodeList

