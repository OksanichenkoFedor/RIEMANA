from res.global_entities.wafer import Wafer
from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays
from res.getero.algorithm.ray_tracing.main_cycle_line_search import process_particles as process_particle_ls
from res.getero.algorithm.ray_tracing.main_cycle_bvh import process_particles as process_particle_bvh
from res.getero.algorithm.main_cycle_old import process_particles as process_particle_old
from res.getero.algorithm.monte_carlo import generate_particles
from res.getero.algorithm.ray_tracing.bvh import build_BVH

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
    X, Y = give_line_arrays(c_wafer.border_arr)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect(1)
    ax.set_ylim([np.array(Y).max(), np.array(Y).min()])
    x_ticks = np.arange(0, c_wafer.xsize, 1)
    y_ticks = np.arange(0, c_wafer.ysize, 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid()

    ax.plot(X, Y)
    return ax
    #ax.plot(arr_x,arr_y,color="r")





def test_speed_rt(c_wafer,num_particles=100, do_plot=False, do_plot_stat=False):
    params = generate_particles(num_particles, c_wafer.xsize,y_ar_plus=y_ar_plus, y_cl=y_cl, y_cl_plus=y_cl_plus, T_i=T_i, T_e=U_i, y0=c_wafer.y0)
    Times1 = []
    Times2 = []
    Times3 = []
    NodeList = build_BVH(c_wafer.border_arr)
    if do_plot:
        ax = plot_wafer(c_wafer)
    ls, bvh = 0, 0
    for i in trange(len(params)):
        params_arr = params[i]
        #print(params_arr)
        if y_cl_plus == 0.0:
            R = 1000
        else:
            R = y_cl / y_cl_plus
        t1 = time.time_ns()
        _, arr_x_ls, arr_y_ls, _, _ = process_particle_ls(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.border_arr,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R,True, c_wafer.is_half)
        t2 = time.time_ns()
        Times1.append(t2-t1)
        t1 = time.time_ns()
        _, arr_x_old, arr_y_old, _, _ = process_particle_old(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.border_arr,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half)
        t2 = time.time_ns()
        Times2.append(t2 - t1)
        t1 = time.time_ns()
        _, arr_x_bvh, arr_y_bvh, _, _ = process_particle_bvh(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.border_arr, NodeList,
            [params_arr], c_wafer.Si_num, c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half)
        t2 = time.time_ns()
        Times3.append(t2 - t1)
        if arr_x_bvh!=arr_x_ls or arr_y_bvh!=arr_y_ls:
            print("Ошибка!!!")
        if do_plot:
            if Times1[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_ls, arr_y_ls,color="r")
                ls+=1
            if Times3[-1] > 9 * 10 ** 5 or True:
                ax.plot(arr_x_bvh, arr_y_bvh, color=(0, 0, 1, 0.5))
                bvh+=1
    Times1 = np.array(Times1)[1:]
    Times2 = np.array(Times2)[1:]
    Times3 = np.array(Times3)[1:]
    print("ls: ",ls, " bvh: ",bvh)
    if do_plot:
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


def del_some_structure(c_wafer, num_del = 100, seed=10):
    np.random.seed(seed)
    X_del = []
    Y_del = []
    for i in range(num_del):
        X, Y = give_line_arrays(c_wafer.border_arr)
        unfound = True
        while unfound:
            j = np.random.randint(0,len(X))
            curr_x = X[j]
            curr_y = Y[j]
            if c_wafer.is_full[curr_x,curr_y]==1:
                unfound = False
        c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
        c_wafer.is_full[curr_x, curr_y] = 0
        delete_point(c_wafer.border_arr, curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del

def create_some_structure(c_wafer, num_crt = 100, seed=10):
    np.random.seed(seed)
    X_del = []
    Y_del = []
    for i in range(num_crt):
        X, Y = give_line_arrays(c_wafer.border_arr)
        unfound = True
        while unfound:
            j = np.random.randint(0,len(X))
            curr_x = X[j]
            curr_y = Y[j]
            if c_wafer.is_full[curr_x,curr_y]==1:
                unfound = False
        c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
        c_wafer.is_full[curr_x, curr_y] = 0
        delete_point(c_wafer.border_arr, curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del
if True:
    multiplier, Si_num = 0.1, 84
    test_ray_tracing_params = {
        "mask_height": 200,
        "hole_size": 200,
        "border": 500,
        "xsize": 1000,
        "ysize": 2400,
        "silicon_size": 1600
    }
    t1 = time.time()
    rt_wafer = Wafer()
    rt_wafer.generate_pure_wafer(multiplier, Si_num, params=test_ray_tracing_params)
    t2 = time.time()
    del_some_structure(rt_wafer,2000, seed=12)
    rt_wafer.check_correction()
    t3 = time.time()
    #X, Y = give_line_arrays(rt_wafer.border_arr)
    #f = generate_figure(rt_wafer, wafer_curr_type="is_cell", do_plot_line=True)
    #plt.show()
end_wafer = Wafer()
end_wafer.load("../files/test_wafer_16000.zip")
#end_wafer.load("../files/wafer_U200_Ar0.5_SiNum84.zip")
test_speed_rt(rt_wafer,num_particles=200, do_plot=True, do_plot_stat=True)


#plt.show()