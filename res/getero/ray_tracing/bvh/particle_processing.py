import numpy as np

from res.getero.ray_tracing.profile_approximation import count_norm_angle
from res.getero.ray_tracing.utils import check_angle_collision, check_if_part_inside, count_angle
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.algorithm.utils import straight_reflection
from res.getero.ray_tracing.bvh.algorithm import bvh_count_collision_point, build_BVH
from res.getero.ray_tracing.line_search.algorithm import simple_count_collision_point
from res.getero.ray_tracing.bvh.collision_functions import count_curr_prev_att
from res.getero.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point, find_close_void


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def process_one_particle(counter_arr, is_full_arr, border_layer_arr, NodeList,
                         returned_particles, arr_x, arr_y, rarr_x, rarr_y,
                         params, Si_num, xsize, ysize, R, test, do_half, max_value, type, num_one_side_points, seed,
                         start_segment=np.ones((2,2))*(-1.0)):
    curr_vec = np.zeros(2)
    curr_vec[0] = params[0]
    curr_vec[1] = params[1]
    start_segment = start_segment
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    unfound = True
    not_max_value = True
    if test:
        pass
        arr_x.append(curr_vec[0] - 0.5)
        arr_y.append(curr_vec[1] - 0.5)
    #print("--- ", curr_type)
    first_time = True
    num = 0
    while unfound and not_max_value:
        num+=1
        if num>1000:
            print("Strange: ", curr_type)
            print([curr_vec[0], curr_vec[1], curr_en, curr_angle, curr_type])
            unfound = False
        #print("start bvh")
        if type=="bvh":
            is_collide, coll_vec, norm_angle, start_segment, cnum = bvh_count_collision_point(NodeList, curr_vec, curr_angle, start_segment)
            #if cnum!=0 and cnum%2==0:
            #    print("Incorrect intersecting segment_particle_processing: ", cnum)
            if first_time:
                pass
                #print(is_collide)
            first_time = False
        else:
            is_collide, coll_vec, norm_angle, start_segment = simple_count_collision_point(border_layer_arr, curr_vec,
                                                                         curr_angle, start_segment)
        if is_collide:
            is_bad_angle = check_if_part_inside(curr_angle, start_segment)
            if is_bad_angle:
                unfound = False
            else:
                if test:
                    pass
                    arr_x.append(coll_vec[0] - 0.5)
                    arr_y.append(coll_vec[1] - 0.5)
                curr_att_x, curr_att_y, prev_att_x, prev_att_y, _ = count_curr_prev_att(coll_vec, start_segment,
                                                                                        curr_angle,
                                                                                        border_layer_arr)
                avg_norm_angle, _, _, _, _, _, _ = count_norm_angle(border_layer_arr, coll_vec, start_segment,
                                                                    do_half, num_one_side_points=num_one_side_points)
                if is_full_arr[prev_att_x, prev_att_y] == 1:
                    print("Граница на пустоте: ", prev_att_x, prev_att_y)
                if (np.abs(coll_vec[0] - xsize) < 10 ** (-5) and do_half) and is_full_arr[
                    curr_att_x, curr_att_y] == 1.0:
                    print("Mirror: ", is_full_arr[curr_att_x, curr_att_y])
                if is_full_arr[curr_att_x, curr_att_y] == 1.0:

                    if border_layer_arr[curr_att_x, curr_att_y, 0] != 1.0:
                        print("ffffff")
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
                    # print("start silicon_reactions")
                    if ((avg_norm_angle < 0.5 * np.pi and avg_norm_angle > 0) or (
                            avg_norm_angle > 1.5 * np.pi)) and curr_type == 0.0:
                        pass
                        # print("---")
                        # print(redepo_params)
                        # print(curr_att_x, curr_att_y, curr_type)
                        # print(counter_arr[:, curr_att_x, curr_att_y])
                    new_type, new_en, flags, redepo_params, new_angle = silicon_reaction(curr_type, counter_arr,
                                                                                         is_full_arr, point_vector,
                                                                                         Si_num, angles, curr_en, R)
                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, start_segment,
                                                               coll_vec, seed)
                    if seed != -1:
                        seed = (seed * 1.534534534) % 1
                    # if curr_type==0 and new_type==0:
                    #    print("Radical:", flags[0])
                    if ((avg_norm_angle < 0.5 * np.pi and avg_norm_angle > 0) or (
                            avg_norm_angle > 1.5 * np.pi)) and curr_type == 0.0:
                        pass
                        # print(counter_arr[:, curr_att_x, curr_att_y])
                    # print("end silicon_reactions")
                    if curr_type in [7, 8, 9] and (not test):
                        # родились бесполезные частицы рассматриваем их только когда тест
                        unfound = False
                        returned_particles[int(curr_type)] += 1
                    if flags[2] == 1.0:
                        # удаление
                        # 0 - внутри
                        # 1 - граница
                        # -1 - снаружи

                        delete_point(border_layer_arr, is_full_arr, curr_att_x, curr_att_y)

                        if type == "bvh":
                            NodeList = build_BVH(border_layer_arr, do_half)
                        # print("Delete: ", curr_att_x, curr_att_y)
                        if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
                            print("Удаление не произведено!")
                        if is_full_arr[curr_att_x, curr_att_y] and not (is_full_arr[curr_att_x, curr_att_y] == -1):
                            print("Непредсказуемое удаление!!!: ", is_full_arr[curr_att_x, curr_att_y])

                    if flags[3] == 1.0:
                        # восстановление частицы
                        print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
                        create_point(border_layer_arr, is_full_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)
                        if type == "bvh":
                            NodeList = build_BVH(border_layer_arr, do_half)
                        new_x, new_y = find_close_void(border_layer_arr, prev_att_x, prev_att_y)
                        coll_vec[0], coll_vec[1] = (prev_att_x + 0.5 + 0.1 * (new_x - prev_att_x),
                                                    prev_att_y + 0.5 + 0.1 * (new_y - prev_att_y))
                        start_segment[0, 0], start_segment[0, 1] = -1, -1
                        start_segment[1, 0], start_segment[1, 1] = -1, -1

                    if flags[1] == 1.0:
                        _, _, _, redepo_params[4]= check_angle_collision(curr_angle, redepo_params[4], start_segment,
                                                                   coll_vec, seed)
                        #left_angle = count_angle(start_segment[0, 1] - start_segment[1, 1],
                        #                         start_segment[0, 0] - start_segment[1, 0])
                        #right_angle = count_angle(start_segment[1, 1] - start_segment[0, 1],
                        #                          start_segment[1, 0] - start_segment[0, 0])
                        #print("redepo start: ", redepo_params[4] / np.pi, left_angle / np.pi,
                        #      right_angle / np.pi)
                        redepo_params[0] = coll_vec[0]
                        redepo_params[1] = coll_vec[1]
                        redepo_params[2] = 0  # is_on_horiz
                        redepo_params[6] = prev_att_x
                        redepo_params[7] = prev_att_y
                        NodeList = process_one_particle(counter_arr, is_full_arr, border_layer_arr, NodeList,
                                                        returned_particles, rarr_x, rarr_y, rarr_x, rarr_y,
                                                        redepo_params,
                                                        Si_num, xsize, ysize, R, test, do_half, max_value, type,
                                                        num_one_side_points, seed, start_segment)
                        #print("redepo end")
                        if is_full_arr[prev_att_x, prev_att_y] == 1:
                            pass
                            print("Ловушка джокера")
                            # prev_att_x, prev_att_y, curr_x, curr_y = throw_particle_away(is_full_arr, prev_att_x,
                            #                                                             prev_att_y,
                            #                                                             curr_x, curr_y)
                    # проверка на то, что после create не произошло попадание в текстуры
                    # is_fall_inside = check_fall_inside(border_layer_arr, curr_vec, NodeList, start_segment)

                    # if is_fall_inside:
                    #    tmp_is_collide, tmp_coll_vec, norm_angle, tmp_start_segment, _ = bvh_count_collision_point(NodeList,
                    #                                                        curr_vec, (curr_angle+np.pi)%(2.0*np.pi),
                    #                                                                                             start_segment)
                    #    start_segment = tmp_start_segment
                    #    coll_vec = tmp_coll_vec

                    curr_angle = new_angle
                    curr_type = new_type
                    curr_en = new_en
                    if flags[0] == 1.0:
                        unfound = False
                elif is_full_arr[curr_att_x, curr_att_y] == 2.0:
                    # Маска
                    new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, start_segment,
                                                               coll_vec, seed)
                    if seed != -1:
                        seed = (seed * 1.534534534) % 1
                    curr_angle = new_angle
                elif is_full_arr[curr_att_x, curr_att_y] == -1.0:
                    # Маска
                    print("Мы ударились о пустоту! ", is_full_arr[curr_att_x, curr_att_y])
                    new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, start_segment,
                                                               coll_vec, seed)
                    if seed != -1:
                        seed = (seed * 1.534534534) % 1
                    curr_angle = new_angle
                else:
                    # print("Мы ударились о пустоту! ", is_full_arr[curr_att_x, curr_att_y])
                    new_angle = straight_reflection(curr_angle, avg_norm_angle)
                    _, _, _, new_angle = check_angle_collision(curr_angle, new_angle, start_segment,
                                                               coll_vec, seed)
                    if seed != -1:
                        seed = (seed * 1.534534534) % 1
                    curr_angle = new_angle
                curr_vec = coll_vec
        else:
            unfound = False
            if test:
                pass
                arr_x.append(curr_vec[0] - 0.5 + np.sin(curr_angle)*500)
                arr_y.append(curr_vec[1] - 0.5 + np.cos(curr_angle)*500)
        #print("end collision processing")
    return NodeList

