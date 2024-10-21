import numpy as np
from res.utils.wrapper import clever_njit
from res.utils.config import do_njit, cache, parallel

from res.getero.ray_tracing.utils import count_angle, give_coefs_line


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def give_part_of_border(border_arr, curr_segment, is_half, num_one_side_points):
    # ищем начало
    #print(curr_segment)
    #print("--- ", is_half)
    reach_left_side = False

    start_x, start_y = int(curr_segment[0, 0] - 0.5), int(curr_segment[0, 1] - 0.5)
    end_x, end_y = int(curr_segment[1, 0] - 0.5), int(curr_segment[1, 1] - 0.5)
    if int(2 * curr_segment[0, 0]) % 2 == 0 and int(2 * curr_segment[1, 0]) % 2 == 0:
        # мы находимся на граничной линии
        #print("Зеркальная граница: ",curr_segment)
        X = np.ones(2 * num_one_side_points + 2) * curr_segment[0, 0]
        Y = 0.5 + np.arange(2*num_one_side_points+2, 0, -1)
        #print(X, Y)
        return X, Y, num_one_side_points, True
    X, Y = np.zeros(2 * num_one_side_points + 2), np.zeros(2 * num_one_side_points + 2)
    X[num_one_side_points], X[num_one_side_points+1] = curr_segment[0,0], curr_segment[1,0]
    Y[num_one_side_points], Y[num_one_side_points+1] = curr_segment[0,1], curr_segment[1,1]

    # start finding prev
    for i in range(num_one_side_points):
        new_x, new_y = border_arr[start_x, start_y, 1], border_arr[start_x, start_y, 2]
        #print(border_arr[start_x, start_y])
        if new_x != -1 or new_y != -1:
            start_x, start_y = new_x, new_y
        X[num_one_side_points - (i + 1)] = start_x + 0.5
        Y[num_one_side_points - (i + 1)] = start_y + 0.5

    if is_half:

        reach_left_side = False
        ind_ls = 0

        for i in range(num_one_side_points):
            if not reach_left_side:
                new_x, new_y = border_arr[end_x, end_y, 3], border_arr[end_x, end_y, 4]
            if (new_x != -1 or new_y != -1):
                end_x, end_y = new_x, new_y
                X[num_one_side_points + 1 + (i + 1)] = end_x + 0.5
                Y[num_one_side_points + 1 + (i + 1)] = end_y + 0.5
            elif not reach_left_side:
                # print("---")
                #print("ГОООЛ!")
                reach_left_side = True
                #if int(2 * curr_segment[0, 0]) % 2 == 0 and int(2 * curr_segment[1, 0]) % 2 == 0:
                #    print("Dno: ", curr_segment[0, 0], curr_segment[0, 1])
                #X = 0.5 + curr_segment[0, 0] +  np.arange(0, 2 * num_one_side_points + 2, 1)
                #Y = np.ones(2 * num_one_side_points + 2) * curr_segment[0, 1]
                ## print(X, Y)
                #return X, Y, num_one_side_points, True

                ind_ls = i - 2

                end_x1, end_y1 = border_arr[end_x, end_y, 1], border_arr[end_x, end_y, 2]
                end_x, end_y = end_x1, end_y1

                end_x1, end_y1 = border_arr[end_x, end_y, 1], border_arr[end_x, end_y, 2]
                end_x, end_y = end_x1, end_y1

                mirror_point_x = end_x + 0.5

        if reach_left_side:
            while ind_ls < num_one_side_points:
                new_x, new_y = border_arr[end_x, end_y, 1], border_arr[end_x, end_y, 2]
                #print(border_arr[end_x, end_y], mirror_point_x, end_y + 0.5, mirror_point_x * 2 - end_x + 0.5)
                X[num_one_side_points + 1 + (ind_ls + 1)] = mirror_point_x * 2 - end_x + 0.5
                Y[num_one_side_points + 1 + (ind_ls + 1)] = end_y + 0.5
                end_x, end_y = new_x, new_y
                ind_ls += 1

    else:
        for i in range(num_one_side_points):
            new_x, new_y = border_arr[end_x, end_y, 3], border_arr[end_x, end_y, 4]
            if new_x != -1 and new_y != -1:
                end_x, end_y = new_x, new_y
            X[num_one_side_points + 1 + (i + 1)] = end_x + 0.5
            Y[num_one_side_points + 1 + (i + 1)] = end_y + 0.5
    if int(2 * curr_segment[0, 0]) % 2 == 0 and int(2 * curr_segment[1, 0]) % 2 == 0:
        print("Incorrect end: ", curr_segment[0, 0], curr_segment[0, 1])
    return X, Y, num_one_side_points, reach_left_side


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_norm_angle(border_arr, cross_vec, curr_segment, is_half, num_one_side_points=5):
    bX, bY, num, reach_left_side = give_part_of_border(border_arr, curr_segment, is_half, num_one_side_points=num_one_side_points)

    mean_dX, mean_dY = np.mean(bX[1:] - bX[:-1]), np.mean(bY[1:] - bY[:-1])
    if mean_dY > 0:
        pass
        #bX = (-1.0)*bX[::-1]
        bX = bX[::-1]
        bY = bY[::-1]

    w = give_coefs_line(bX, bY)

    if mean_dY > 0:

        #w[0] = -1*w[0]

        if mean_dX > 0:
            deb = 1
            #w[1] = -1*w[1]
        else:
            #w[1] = -1 * w[1]
            deb = 2
    else:
        if mean_dX > 0:
            deb = -1
        else:
            deb = -2
    start_norm_angle = count_angle(w[0], w[1])
    #print(w, cross_vec)
    if mean_dY > 0:
        pass
        #bX = (-1.0)*bX[::-1]
        bX = bX[::-1]
        bY = bY[::-1]

    if w[0]*(bX[-1]-bX[0]) - w[1]*(bY[-1]-bY[0])<0:
        norm_angle = start_norm_angle
    else:
        norm_angle = (start_norm_angle+np.pi)%(2*np.pi)
    return norm_angle, deb, bX, bY, w[0], w[1], reach_left_side


@clever_njit(do_njit=do_njit, cache=cache, parallel=parallel)
def count_simple_norm_angle(curr_angle, is_on_horiz):
    if is_on_horiz:
        if curr_angle < 0.5 * np.pi or curr_angle > 1.5 * np.pi:
            angle = np.pi
        else:
            angle = 0
    else:
        if curr_angle < np.pi:
            angle = 1.5 * np.pi
        else:
            angle = 0.5 * np.pi
    #print("Norm: ", curr_angle / np.pi, is_on_horiz, angle / np.pi)
    return angle
