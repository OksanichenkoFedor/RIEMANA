import time
from copy import deepcopy
import numpy as np

from tqdm import trange
from fontTools.subset import intersect
from matplotlib import pyplot as plt

from res.getero.algorithm.dynamic_profile import give_start, delete_point, give_line_arrays, give_coords_from_num, \
    create_point
from res.getero.ray_tracing.utils import count_angle
from res.global_entities.plotter import generate_figure
from res.global_entities.wafer import Wafer


def del_some_structure(c_wafer, num_del = 100, seed=10):
    np.random.seed(seed)
    X_del = []
    Y_del = []
    for i in trange(num_del):
        incorrect_del = True
        while incorrect_del:
            X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
            unfound = True
            while unfound:
                j = np.random.randint(0, len(X))
                curr_x = X[j]
                curr_y = Y[j]
                if c_wafer.is_full[curr_x, curr_y] == 1:
                    unfound = False
            tmp_ba = deepcopy(c_wafer.border_arr)
            tmp_ca = deepcopy(c_wafer.counter_arr)
            tmp_i = deepcopy(c_wafer.is_full)
            tmp_ih = deepcopy(c_wafer.is_hard)
            tmp_as = deepcopy(c_wafer.add_segments)
            c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
            c_wafer.is_full[curr_x, curr_y] = 0
            c_wafer.add_segments = delete_point(c_wafer.border_arr, c_wafer.is_full, c_wafer.is_hard,
                                                c_wafer.add_segments, curr_x, curr_y)
            intersect = c_wafer.check_self_intersection()
            if intersect:
                c_wafer.border_arr = tmp_ba
                c_wafer.counter_arr = tmp_ca
                c_wafer.is_full = tmp_i
                c_wafer.is_hard = tmp_ih
                c_wafer.add_segments = tmp_as
            else:
                incorrect_del = False
            incorrect_del = False
        #print(curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del

def create_some_structure(c_wafer, num_create = 100, seed=10):
    np.random.seed(seed)
    X_crt = []
    Y_crt = []
    for i in trange(num_create):
        incorrect_create = True
        while incorrect_create:
            X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
            unfound = True
            while unfound:
                j = np.random.randint(0, len(X))
                curr_x = X[j]
                curr_y = Y[j]
                if c_wafer.is_full[curr_x, curr_y] == 1:
                    pass
                    unfound_1 = True
                    #print(curr_x, curr_y)
                    js = np.arange(0, 8, 1)
                    np.random.shuffle(js)
                    for i in range(8):
                        if unfound_1:
                            j1 = js[i]
                            new_x, new_y = give_coords_from_num(j1, curr_x, curr_y)
                            if c_wafer.border_arr[new_x, new_y, 0] == -1 and (
                                    possible_to_reach(c_wafer.border_arr, curr_x, curr_y, new_x, new_y) or (
                                    not c_wafer.is_hard[new_x, new_y])):
                                # if (new_x==221 and new_y==141) and (curr_x==222 and curr_y==141):
                                #    print("possible_to_reach: ",possible_to_reach(c_wafer.border_arr, curr_x, curr_y, new_x, new_y))
                                unfound_1 = False
                    if not unfound_1:
                        unfound = False



                    #print(c_wafer.is_hard[new_x, new_y])
            tmp_ba = deepcopy(c_wafer.border_arr)
            tmp_ca = deepcopy(c_wafer.counter_arr)
            tmp_i = deepcopy(c_wafer.is_full)
            tmp_ih = deepcopy(c_wafer.is_hard)
            tmp_as = deepcopy(c_wafer.add_segments)
            #c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
            c_wafer.is_full[new_x, new_y] = 1
            print("Create: ",new_x, new_y, curr_x, curr_y)
            c_wafer.add_segments = create_point(c_wafer.border_arr, c_wafer.is_full, c_wafer.is_hard,
                                                c_wafer.add_segments, new_x, new_y, curr_x, curr_y)
            c_wafer.check_correction()
            #c_wafer.add_segments = delete_point(c_wafer.border_arr, c_wafer.is_full, c_wafer.is_hard,
            #                                    c_wafer.add_segments, curr_x, curr_y)
            intersect = c_wafer.check_self_intersection()
            if intersect:
                c_wafer.border_arr = tmp_ba
                c_wafer.counter_arr = tmp_ca
                c_wafer.is_full = tmp_i
                c_wafer.is_hard = tmp_ih
                c_wafer.add_segments = tmp_as
            else:
                incorrect_create = False
            incorrect_create = False
        # print(curr_x, curr_y)
        X_crt.append(new_x)
        Y_crt.append(new_y)
    return X_crt, Y_crt

def possible_to_reach(border_arr,curr_x, curr_y, new_x, new_y):
    if border_arr[curr_x, curr_y, 1] == -1 and border_arr[curr_x, curr_y, 2] == -1:
        prev_x, prev_y = curr_x + 0.0, curr_y + 0.5
    else:
        prev_x, prev_y = border_arr[curr_x, curr_y, 1] + 0.5, border_arr[curr_x, curr_y, 2] + 0.5

    if border_arr[curr_x, curr_y, 3] == -1 and border_arr[curr_x, curr_y, 4] == -1:
        next_x, next_y = curr_x + 1.0, curr_y + 0.5
    else:
        next_x, next_y = border_arr[curr_x, curr_y, 3] + 0.5, border_arr[curr_x, curr_y, 4] + 0.5
    curr_x, curr_y, new_x, new_y = curr_x + 0.5, curr_y + 0.5, new_x + 0.5, new_y + 0.5
    left_angle = count_angle(prev_y - curr_y, prev_x - curr_x)
    right_angle = count_angle(next_y - curr_y, next_x - curr_x)
    new_angle = count_angle(new_y - curr_y, new_x - curr_x)
    #print(left_angle/np.pi, right_angle/np.pi, new_angle/np.pi)
    if (new_angle/np.pi-right_angle/np.pi)%2+(left_angle/np.pi-new_angle/np.pi)%2==(left_angle/np.pi-right_angle/np.pi)%2:
        return True
    else:
        return False

def defend_wafer(c_wafer):
    x, y = give_start(c_wafer.border_arr)
    y_max = y
    unfound = True
    while unfound:
        y_max = max(y, y_max)
        x, y = c_wafer.border_arr[x, y, 3], c_wafer.border_arr[x, y, 4]
        if x == -1 and y == -1:
            unfound = False
        else:
            c_wafer.is_full[x, y] = 2.0


def create_test_wafer(num_del=2000, num_create=100, seed=12, multiplier=0.1, start_wafer=None):
    if start_wafer is None:
        multiplier, Si_num = multiplier, 84
        test_ray_tracing_params = {
            "mask_height": 200,
            "hole_size": 200,
            "border": 500,
            "xsize": 1000,
            "ysize": 1200,
            "silicon_size": 1600
        }
        t1 = time.time()
        rt_wafer = Wafer()
        rt_wafer.generate_pure_wafer(multiplier, Si_num, params=test_ray_tracing_params)
        t2 = time.time()
    else:
        rt_wafer = start_wafer
    del_some_structure(rt_wafer, num_del=num_del, seed=seed)
    create_some_structure(rt_wafer, num_create=num_create, seed=seed)
    #defend_wafer(rt_wafer)
    rt_wafer.check_correction()
    t3 = time.time()
    # X, Y = give_line_arrays(rt_wafer.border_arr)
    #f = generate_figure(rt_wafer, wafer_curr_type="is_cell", do_plot_line=True)
    #plt.show()
    return rt_wafer