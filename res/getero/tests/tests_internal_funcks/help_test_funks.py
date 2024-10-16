import time
from copy import deepcopy
import numpy as np

from tqdm import trange
from fontTools.subset import intersect
from matplotlib import pyplot as plt

from res.getero.algorithm.dynamic_profile import give_start, delete_point, give_line_arrays
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
            c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
            c_wafer.is_full[curr_x, curr_y] = 0
            c_wafer.add_segments = delete_point(c_wafer.border_arr, c_wafer.is_full, c_wafer.is_hard,
                                                c_wafer.add_segments, curr_x, curr_y)
            intersect = c_wafer.check_self_intersection()
            if intersect:
                c_wafer.border_arr = tmp_ba
                c_wafer.counter_arr = tmp_ca
                c_wafer.is_full = tmp_i
            else:
                incorrect_del = False
            incorrect_del = False
        #print(curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del

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


def create_test_wafer(num_del=2000, seed=12):
    multiplier, Si_num = 0.1, 84
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
    del_some_structure(rt_wafer, num_del=num_del, seed=seed)
    defend_wafer(rt_wafer)
    rt_wafer.check_correction()
    t3 = time.time()
    # X, Y = give_line_arrays(rt_wafer.border_arr)
    #f = generate_figure(rt_wafer, wafer_curr_type="is_cell", do_plot_line=True)
    #plt.show()
    return rt_wafer