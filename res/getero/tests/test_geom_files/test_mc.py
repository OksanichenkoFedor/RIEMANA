import numpy as np
import matplotlib.pyplot as plt
import numba as nb

from matplotlib.patches import Circle

from res.getero.algorithm.space_orientation import find_next, give_next_cell, throw_particle_away

from res.getero.algorithm.silicon_reactions.silicon_reactions import silicon_reaction
from res.getero.algorithm.mask_reactions import mask_reaction
from res.getero.algorithm.dynamic_profile import delete_point, create_point

from res.getero.algorithm.ray_tracing.profile_approximation import give_part_of_border, line_approximation, is_collide


def process_one_particle(counter_arr, is_full_arr, border_layer_arr, params, Si_num, xsize, ysize, R, test, max_value, axis):
    arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                   nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    returned_particles = nb.typed.List.empty_list(nb.int8)
    curr_x = params[0]
    curr_y = params[1]
    is_on_horiz = params[2]
    curr_en = params[3]
    curr_angle = params[4]
    curr_type = params[5]
    prev_att_x = int(params[6])
    prev_att_y = int(params[7])
    prev_y, prev_x = None, None
    unfound = True
    changed_angle = False
    num = 0
    unfound_test = True
    not_max_value = True
    Prev_x = nb.typed.List.empty_list(nb.f8)
    Prev_y = nb.typed.List.empty_list(nb.f8)
    p_a_x = nb.typed.List.empty_list(nb.f8)
    p_a_y = nb.typed.List.empty_list(nb.f8)
    Curr_x = nb.typed.List.empty_list(nb.f8)
    Curr_y = nb.typed.List.empty_list(nb.f8)
    c_a_x = nb.typed.List.empty_list(nb.f8)
    c_a_y = nb.typed.List.empty_list(nb.f8)
    ifa_p = nb.typed.List.empty_list(nb.f8)
    ifa_c = nb.typed.List.empty_list(nb.f8)
    while unfound and not_max_value:

        if max_value != -1.0:
            if num > max_value:
                not_max_value = False
        num += 1
        curr_att_x, curr_att_y = find_next(curr_x, curr_y, prev_x, prev_y, prev_att_x, prev_att_y)
        fig, ax = plt.subplots(figsize=(10, 10))
        print("curr2: ", curr_x, curr_y, curr_angle / np.pi)
        ax.arrow(curr_x, curr_y, 0.5 * np.sin(curr_angle), 0.5 * np.cos(curr_angle), color="k")
        ax.plot([curr_att_x, curr_att_x + 1, curr_att_x + 1, curr_att_x, curr_att_x],
                [curr_att_y, curr_att_y, curr_att_y + 1, curr_att_y + 1, curr_att_y],
                color="r")
        ax.invert_yaxis()
        ax.set_aspect(1)
        plt.show()
        #if prev_x is None:
        #    Prev_x.append(0)
        #    Prev_y.append(0)
        #else:
        #    Prev_x.append(prev_x)
        #    Prev_y.append(prev_y)
        #p_a_x.append(prev_att_x)
        #p_a_y.append(prev_att_y)
        #Curr_x.append(curr_x)
        #Curr_y.append(curr_y)
        #c_a_x.append(curr_att_x)
        #c_a_y.append(curr_att_y)
        #ifa_p.append(is_full_arr[prev_att_x, prev_att_y])
        #ifa_c.append(is_full_arr[curr_att_x, curr_att_y])
        if (curr_att_x == prev_att_x and curr_att_y == prev_att_y) and (not (prev_y is None)):
            pass
            print("Ахтунг!!!!")
            print(curr_x, curr_y, prev_x, prev_y)
            print(curr_att_x, prev_att_x, curr_att_y, prev_att_y)
            print(curr_angle, curr_angle / np.pi)
            print(is_full_arr[curr_att_x, curr_att_y])
        # print(curr_att_x, curr_att_y)

        if is_full_arr[curr_att_x, curr_att_y] == 1.0:
            if prev_y is None:
                print("NONE")
                do_collide = is_collide(curr_x, curr_y, arc_x, arc_y, curr_att_x, curr_att_y, border_layer_arr, curr_angle)
            else:
                do_collide = is_collide(curr_x, curr_y, prev_x, prev_y, curr_att_x, curr_att_y, border_layer_arr, curr_angle)
        else:
            do_collide = False

        if do_collide:
            if (num > 10000 and unfound_test):
                if curr_type == 9.0:
                    print("Argon in silicon cage!")
                    return arr_x, arr_y, rarr_x, rarr_y, returned_particles
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
            #n_angle = count_norm_angle(border_layer_arr, curr_att_x, curr_att_y, curr_x, curr_y, prev_x, prev_y)
            print("---")
            print("Start_angle: ", curr_angle/np.pi)
            n_angle = test_n(border_layer_arr, curr_att_x, curr_att_y, 2, curr_x, curr_y, prev_x, prev_y, axis)
            new_type, new_curr_counter, new_prev_counter, new_curr_farr, new_prev_farr, is_react, new_angle, \
            new_en, is_redepo, redepo_params = silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr,
                                                                prev_farr, Si_num, n_angle, curr_angle, curr_en,
                                                                R)
            print("New_angle: ", new_angle / np.pi)
            if curr_type in [7, 8, 9] and (not test):
                # родились бесполезные частицы рассматриваем их только когда тест
                #print("---")
                unfound = False
                returned_particles.append(int(curr_type))
            if new_curr_farr != curr_farr:
                # удаление
                # 0 - внутри
                # 1 - граница
                # -1 - снаружи
                #print("Delete: ", curr_att_x, curr_att_y)
                delete_point(border_layer_arr, curr_att_x, curr_att_y)
                if border_layer_arr[curr_att_x, curr_att_y, 0] == 1:
                    print("Удаление не произведено!")
                if new_curr_farr:
                    print("Непредсказуемое удаление!!!")

            if new_prev_farr != prev_farr:
                # восстановление частицы
                #print("Create: ", prev_att_x, prev_att_y, " from: ", curr_att_x, curr_att_y)
                create_point(border_layer_arr, prev_att_x, prev_att_y, curr_att_x, curr_att_y)
            counter_arr[:, curr_att_x, curr_att_y] = new_curr_counter
            counter_arr[:, prev_att_x, prev_att_y] = new_prev_counter
            is_full_arr[curr_att_x, curr_att_y] = new_curr_farr
            is_full_arr[prev_att_x, prev_att_y] = new_prev_farr
            curr_angle = new_angle
            curr_type = new_type
            curr_en = new_en

            if is_redepo:
                old_curr_val = is_full_arr[prev_att_x, prev_att_y]
                redepo_params[0] = curr_x
                redepo_params[1] = curr_y
                redepo_params[2] = is_on_horiz
                redepo_params[4] = redepo_params[4] / np.pi
                redepo_params[6] = prev_att_x
                redepo_params[7] = prev_att_y
                redepo_params[4] = redepo_params[4] * np.pi
                arr_x_1, arr_y_1, arr_x_2, arr_y_2, new_returned_particles = process_one_particle(counter_arr,
                                                                                                  is_full_arr,
                                                                                                  border_layer_arr,
                                                                                                  redepo_params, Si_num,
                                                                                                  xsize, ysize, R, test,
                                                                                                  max_value, axis)

                rarr_x = unite_lists(unite_lists(rarr_x, arr_x_1), arr_x_2)
                rarr_y = unite_lists(unite_lists(rarr_y, arr_y_1), arr_y_2)
                returned_particles = unite_lists(returned_particles, new_returned_particles)
                if is_full_arr[prev_att_x, prev_att_y] == 1:
                    if old_curr_val != 0:
                        print("Или я тупой или лыжи не едут!")
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
            if border_layer_arr[curr_att_x, curr_att_y, 0] != -1:
                pass
                #print("Некорректный расчёт профиля! ", border_layer_arr[curr_att_x, curr_att_y, 0])
            prev_x = curr_x
            prev_y = curr_y
            prev_att_x, prev_att_y = curr_att_x, curr_att_y

            curr_x, curr_y, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)



            if test:
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)

            is_on_horiz = new_is_on_horiz

            if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                unfound = False
                returned_particles.append(int(curr_type))
            elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                unfound = False
                returned_particles.append(int(curr_type))

        if changed_angle:
            if is_full_arr[prev_att_x, prev_att_y]:
                if border_layer_arr[curr_att_x, curr_att_y, 0] != -1:
                    pass
                    #print("Некорректный расчёт профиля! ", border_layer_arr[curr_att_x, curr_att_y, 0])
                prev_x = curr_x
                prev_y = curr_y
                prev_att_x, prev_att_y = curr_att_x, curr_att_y

                curr_x, curr_y, new_is_on_horiz = give_next_cell(prev_x, prev_y, curr_angle, is_on_horiz)



                if test:
                    arr_x.append(curr_x - 0.5)
                    arr_y.append(curr_y - 0.5)

                is_on_horiz = new_is_on_horiz

                if (curr_x >= xsize or curr_x < 0) or (curr_y >= ysize or curr_y < 0):
                    unfound = False
                    returned_particles.append(int(curr_type))
                elif int(curr_y) <= 1 and (curr_angle <= 1.5 * np.pi and curr_angle >= 0.5 * np.pi):
                    unfound = False
                    returned_particles.append(int(curr_type))
            else:
                arc_x, arc_y = prev_x, prev_y
                prev_x, prev_y = None, None
            #if (is_full_arr[prev_att_x, prev_att_y] and unfound_test):
            #    print("Everlasting reaction")
            #    for i in range(len(Prev_x)):
            #        print("---")
            #        print(Prev_x[i], Prev_y[i], p_a_x[i], p_a_y[i])
            #        print(Curr_x[i], Curr_y[i], c_a_x[i], c_a_y[i])
            #        print(ifa_p[i], ifa_c[i])
            #    print("После отражения мы внутри!!! ", curr_type)
            #    print(prev_att_x, prev_att_y)
            #    print(curr_att_y, curr_att_y)
            #    print(prev_x, prev_y)
            #    print([curr_x, curr_y, is_on_horiz, curr_en, curr_angle, curr_type, prev_att_x, prev_att_y])
            #    print([params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]])
            #    unfound_test = False

            if test:
                arr_x.append(curr_x - 0.5)
                arr_y.append(curr_y - 0.5)
            changed_angle = False

    return arr_x, arr_y, rarr_x, rarr_y, returned_particles



def process_particles(counter_arr, is_full_arr, border_layer_arr, params_arr, Si_num, xsize, ysize, R, test, axis,
                      max_value=-1.0):
    arr_x, arr_y, rarr_x, rarr_y = nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8), \
                                   nb.typed.List.empty_list(nb.f8), nb.typed.List.empty_list(nb.f8)
    returned_particles = nb.typed.List.empty_list(nb.int8)
    for i in range(len(params_arr)):
        curr_params_arr = params_arr[i]
        arr_x_1, arr_y_1, rarr_x_1, rarr_y_1, new_returned_particles = \
            process_one_particle(counter_arr, is_full_arr, border_layer_arr,
                                 curr_params_arr, Si_num, xsize, ysize, R, test, max_value, axis)

        arr_x = unite_lists(arr_x, arr_x_1)
        arr_y = unite_lists(arr_y, arr_y_1)
        rarr_x = unite_lists(rarr_x, rarr_x_1)
        rarr_y = unite_lists(rarr_y, rarr_y_1)
        returned_particles = unite_lists(returned_particles, new_returned_particles)
    return arr_x, arr_y, rarr_x, rarr_y, returned_particles


def unite_lists(a, b):
    for i in range(len(b)):
        a.append(b[i])
    return a

def give_coords(x, A, B):
    return x, (1-A*x)/B

def give_coefs(x, y):
    X = np.ones((x.shape[0], 2))
    X[:, 0] = x
    X[:, 1] = y
    w = np.linalg.pinv(X) @ np.ones((x.shape[0], 1))[:,0]
    return w

def test_n(border_arr, target_x, target_y, num_one_side_points, curr_x, curr_y, prev_x, prev_y, master):
    #alpha = (curr_y - prev_y) / (curr_x - prev_x)
    #beta = (curr_x * prev_y - curr_y * prev_x) / (curr_x - prev_x)

    #def plot_start_line(x):
    #    return alpha * x + beta

    #xt1 = np.arange(prev_x, prev_x + 15 * (curr_x - prev_x), 0.1 * np.sign(curr_x - prev_x))
    # print(curr_x, curr_y, prev_x, prev_y)
    # print(xt1)
    master.ax.plot(curr_x, curr_y, "o", color="g")
    master.ax.plot(prev_x, prev_y, "o", color="b")
    #master.ax.plot(xt1, plot_start_line(xt1), color = (0.5,0.5,0))
    bX, bY, num = give_part_of_border(border_arr, target_x, target_y, num_one_side_points)
    # c, b, a, tp = give_mnk(bX, bY)
    #print(bX.shape)
    for i in range(len(bX)):
        r = 0.5
        if i == num:
            r = 1.0
        circ = Circle((bX[i], bY[i]), r, color="g")
        master.ax.add_patch(circ)
    #A, B, C, D, E = give_coefs(bX, bY)[:,0]
    A, B = give_coefs(bX, bY)
    tp = np.abs(np.max(bY) - np.min(bY)) < np.abs(np.max(bX) - np.min(bX))
    if tp:
        X, Y = give_coords(np.arange(np.min(bX), np.max(bX), 0.1), A, B)
    else:
        Y, X = give_coords(np.arange(np.min(bY), np.max(bY), 0.1), B, A)
    master.ax.plot(X, Y, ".", color="k")
    print("LA: ", curr_x, curr_y, prev_x, prev_y, A, B)
    n_angle, x1, y1 = line_approximation(curr_x, curr_y, prev_x, prev_y, A, B, 1)
    print("LA return: ", n_angle/np.pi, x1, y1)
    master.ax.plot(x1, y1, "o", color="r")
    master.ax.arrow(x1, y1, 5*np.sin(n_angle), 5*np.cos(n_angle), color="b")
    master.canvas.draw()
    return n_angle

    # if tp:
    #    YY = np.arange(np.min(bY) - 1, np.max(bY) + 1, 0.1)
    #    XX = a * YY * YY + b * YY + c
    # else:
    #    XX = np.arange(np.min(bX) - 1, np.max(bX) + 1, 0.1)
    #    YY = a * XX * XX + b * XX + c
    #
    #
    # print(tp)
    # n_angle, x1, y1 = give_norm_angle(curr_x, curr_y, prev_x, prev_y, a, b, c, tp)
    # print(n_angle/np.pi)
    # ax.plot(x1,y1,"o",color="r")
    # ax.arrow(x1,y1, 5*np.sin(n_angle), 5*np.cos(n_angle), color="b")
