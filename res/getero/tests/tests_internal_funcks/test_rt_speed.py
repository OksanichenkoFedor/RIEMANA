from copy import deepcopy

from res.getero.ray_tracing.bvh.algorithm import build_BVH
from res.getero.tests.tests_internal_funcks.help_test_funks import defend_wafer
from res.global_entities.plotter import generate_figure
from res.global_entities.wafer import Wafer, prepare_segment_for_intersection_checking
from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays
from res.getero.algorithm.main_cycle import process_particles
from res.getero.algorithm.monte_carlo import generate_particles
from res.getero.tests.tests_internal_funcks.help_test_funks import create_test_wafer

import res.utils.config as config

from tqdm import trange
import time
import matplotlib.pyplot as plt
import numpy as np



params = config.plasma_params

n_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

y_ar_plus = params["j_ar_plus"]/n_full
y_cl = params["j_cl"]/n_full
y_cl_plus = params["j_cl_plus"]/n_full
cell_size = params["cell_size"]
T_i = params["T_i"]
U_i = params["U_i"]

def plot_wafer(c_wafer):
    X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect(1)
    ax.set_ylim([np.array(Y).max(), max(np.array(Y).min(),0.5)])
    ax.set_xlim([0,c_wafer.xsize])
    x_ticks = np.arange(0, c_wafer.xsize, 1)+0.5
    y_ticks = np.arange(0, c_wafer.ysize, 1)+0.5
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid()

    ax.plot(X, Y)
    return ax
    #ax.plot(arr_x,arr_y,color="r")


def process_str_particle(curr_str):
    curr_str = curr_str.replace("\n", "")
    curr_str = curr_str[1:-1].split()
    res = []
    for i in range(len(curr_str)):
        res.append(float(curr_str[i]))
    print(res)
    return np.array(res)

def compare_arrays(x1, y1, x2, y2):
    if len(x1) == len(x2):
        delta = np.array(x1[1:-1]) - np.array(x2[1:-1])
        if len(delta) > 0:
            delta = np.linalg.norm(delta, ord=np.inf)
        else:
            delta = 0
        if delta > 10 ** (-5):

            num = 0
            while num < len(x1):
                if y1[num] < 0.5:
                    x1.pop(num)
                    y1.pop(num)
                else:
                    num += 1

            num = 0
            while num < len(x2):
                if y2[num] < 0.5:
                    x2.pop(num)
                    y2.pop(num)
                else:
                    num += 1
            delta1 = np.array(x1[1:-1]) - np.array(x2[1:-1])
            delta2 = np.array(y1[1:-1]) - np.array(y2[1:-1])
            if len(delta1) > 0:
                delta = np.linalg.norm(delta1, ord=np.inf)+np.linalg.norm(delta2, ord=np.inf)
            else:
                delta = 0
    else:
        num = 0
        while num < len(x1):
            if y1[num] < 0.5:
                x1.pop(num)
                y1.pop(num)
            else:
                num += 1

        num = 0
        while num < len(x2):
            if y2[num] < 0.5:
                x2.pop(num)
                y2.pop(num)
            else:
                num += 1
        x1, y1 = prepare_segment_for_intersection_checking(x1, y1, None, None, None, None)
        x2, y2 = prepare_segment_for_intersection_checking(x2, y2, None, None, None, None)

    if len(x1) == len(x2):
        delta1 = np.array(x1[1:-1]) - np.array(x2[1:-1])
        delta2 = np.array(y1[1:-1]) - np.array(y2[1:-1])
        if len(delta1) > 0:
            delta = np.linalg.norm(delta1, ord=np.inf) + np.linalg.norm(delta2, ord=np.inf)
        else:
            delta = 0
        if delta > 10 ** (-5):
            return True
    else:
        return True
    return False

def test_speed_rt(c_wafer,num_particles=100, do_plot=False, do_plot_stat=False):
    params = generate_particles(num_particles, c_wafer.xsize,y_ar_plus=y_ar_plus, y_cl=y_cl, y_cl_plus=y_cl_plus, T_i=T_i, T_e=U_i, y0=c_wafer.y0)
    Times1 = []
    Times2 = []
    Times3 = []
    if do_plot:
        ax = plot_wafer(c_wafer)
    ls, bvh, old = 0, 0, 0
    NodeList = build_BVH(c_wafer.border_arr, c_wafer.is_half)
    for i in trange(len(params)):
        params_arr = params[i]
        #params_arr = process_str_particle("[2.00244091e+02 1.00000000e+00 1.00000000e+00 1.20000000e-01 6.08996930e+00 0.00000000e+00 2.00000000e+02 1.00000000e+00]")
        #print(params_arr)
        if y_cl_plus == 0.0:
            R = 1000
        else:
            R = y_cl / y_cl_plus
        seed = np.random.random()
        #print(seed)
        t1 = time.time_ns()
        #print("start cbc old")
        _, arr_x_old, arr_y_old, _, _, _, _ = process_particles(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.is_hard, c_wafer.add_segments, c_wafer.border_arr,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half,
            type="cell by cell", num_one_side_points=config.num_one_side_points, seed=seed)
        #print("end cbc old")
        t2 = time.time_ns()
        Times1.append(t2-t1)
        t1 = time.time_ns()
        #print("start cbc")
        _, arr_x_cbc, arr_y_cbc, _, _, _, _ = process_particles(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.is_hard, c_wafer.add_segments, c_wafer.border_arr,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half,
            type="cell by cell", num_one_side_points=config.num_one_side_points, seed=seed)
        #print("end cbc")
        arr_x_cbc, arr_y_cbc = prepare_segment_for_intersection_checking(arr_x_cbc, arr_y_cbc, None, None, None, None)

        t2 = time.time_ns()
        Times2.append(t2 - t1)
        t1 = time.time_ns()
        #print(c_wafer.nodelist is None)
        #print("start bvh")
        _, arr_x_bvh, arr_y_bvh, _, _, NodeList, c_wafer.add_segments = process_particles(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.is_hard, c_wafer.add_segments, c_wafer.border_arr,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half,
            type="bvh", NodeList=NodeList, num_one_side_points=config.num_one_side_points, seed=seed)
        #print("end bvh")
        t2 = time.time_ns()
        Times3.append(t2 - t1)
        #print(type(list(arr_x_old)))
        arr_x_bvh1, arr_y_bvh1, arr_x_cbc1, arr_y_cbc1 = deepcopy(list(arr_x_bvh)), deepcopy(list(arr_y_bvh)), deepcopy(list(arr_x_cbc)), deepcopy(list(arr_y_cbc))
        is_bad = compare_arrays(arr_x_bvh1, arr_y_bvh1, arr_x_cbc1, arr_y_cbc1)
        if is_bad:
            print("Ошибка!!!")
            print(params_arr)
            print(seed)
            if Times3[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_bvh, arr_y_bvh, color=(0, 0, 1, 0.5))
                bvh += 1
            if Times3[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_cbc, arr_y_cbc, color=(0, 1, 0, 0.5))
                old += 1

        if do_plot and False:
            #if Times1[-1] > 9 * 10 ** 5 or True:
            #    ax.plot(arr_x_ls, arr_y_ls,color="r")
            #    ls+=1
            if Times3[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_bvh, arr_y_bvh, color=(0, 0, 1, 0.5))
                bvh+=1
            if Times3[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_cbc, arr_y_cbc, color=(0, 1, 0, 0.5))
                old += 1
    Times1 = np.array(Times1)[1:]
    Times2 = np.array(Times2)[1:]
    Times3 = np.array(Times3)[1:]
    print("ls: ",ls, " bvh: ",bvh)
    if do_plot:
        X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
        ax.set_ylim([np.array(Y).max(), 0.5])
        plt.show()
    if do_plot_stat:
        fig, (ax_low, ax_up) = plt.subplots(1, 2, figsize=(13, 11))
        process_result_time(Times1,"line_search",ax_low,ax_up)
        process_result_time(Times2, "old", ax_low, ax_up)
        process_result_time(Times3, "bvh", ax_low, ax_up)
        ax_low.legend()
        ax_up.legend()
        ax_low.set_xscale("log")
        ax_up.set_xscale("log")
        plt.show()


def process_result_time(curr_time, label, ax1, ax2, n_bins=20):
    mean = curr_time.mean()
    low_part = curr_time[curr_time<mean]
    up_part = curr_time[curr_time>mean]
    low_str = str(len(low_part))+" "+str(round(np.mean(low_part), 3)) + " +- " + str(round(np.std(low_part), 3))+"нс"
    up_str = str(len(up_part))+" "+str(round(np.mean(up_part) * 0.001, 1)) + " +- " + str(round(np.std(up_part) * 0.001, 1)) + "мкс"
    all_str = str(round(np.mean(curr_time) * 0.001, 1)) + " +- " + str(round(np.std(curr_time) * 0.001, 1)) + "мкс"
    print('Вpемя '+label+': ' + low_str + " " + up_str + " " + all_str)
    ax1.hist(low_part, label=label, bins=n_bins)
    ax2.hist(up_part, label=label, bins=n_bins)

def create_some_structure(c_wafer, num_crt = 100, seed=10):
    np.random.seed(seed)
    X_del = []
    Y_del = []
    for i in range(num_crt):
        X, Y = give_line_arrays(c_wafer.border_arr, c_wafer.is_half)
        unfound = True
        while unfound:
            j = np.random.randint(0,len(X))
            curr_x = X[j]
            curr_y = Y[j]
            if c_wafer.is_full[curr_x,curr_y]==1:
                unfound = False

        c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
        c_wafer.is_full[curr_x, curr_y] = 0
        c_wafer.add_segments = delete_point(c_wafer.border_arr, c_wafer.is_full, c_wafer.is_hard,
                                            c_wafer.add_segments, curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del
if False:
    multiplier, Si_num = 0.1, 84
    test_ray_tracing_params = {
        "mask_height": 200,
        "hole_size": 200,
        "border": 500,
        "xsize": 2000,
        "ysize": 2400,
        "silicon_size": 1600
    }
    t1 = time.time()
    rt_wafer = Wafer()
    rt_wafer.generate_pure_wafer(multiplier, Si_num, params=test_ray_tracing_params)
    t2 = time.time()
    del_some_structure(rt_wafer,2000, seed=12)
    defend_wafer(rt_wafer)
    rt_wafer.check_correction()
    t3 = time.time()
    #X, Y = give_line_arrays(rt_wafer.border_arr)
    f = generate_figure(rt_wafer, wafer_curr_type="is_cell", do_plot_line=True)
    plt.show()
end_wafer = Wafer()
#end_wafer.load("../files/test_just_delete.zip")
end_wafer.load("../files/test_create.zip")
end_wafer = create_test_wafer(num_del=0, num_create=0, multiplier=0.2, start_wafer=end_wafer)
#end_wafer.save("../files/1000_del_02_mult.zip")
#end_wafer = Wafer()
#end_wafer = create_test_wafer(num_del=5000, multiplier=0.2)
#end_wafer.save("../files/test_create.zip")
#end_wafer.save("../files/test_just_delete.zip")
#end_wafer.load("../files/5000_del_02_mult.zip")
#end_wafer.make_half()
defend_wafer(end_wafer)
#end_wafer.load("../files/tmp_U200_1000_1.zip")


#end_wafer.load("../files/wafer_U40_Ar0.5_SiNum30.zip")

#end_wafer.load("../files/tmp_U200_2000_2.zip")
f = generate_figure(end_wafer, wafer_curr_type="is_cell", do_plot_line=True)
#plt.show()
#end_wafer.make_half()
test_speed_rt(end_wafer,num_particles=500, do_plot=True, do_plot_stat=False)


#plt.show()