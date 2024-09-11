from res.global_entities.wafer import Wafer
from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays
from res.getero.algorithm.ray_tracing.main_cycle import process_particles
from res.getero.algorithm.ray_tracing_sbs import process_particles as p_p_old
from res.getero.algorithm.monte_carlo import generate_particles

import res.utils.config as config

import time
import matplotlib.pyplot as plt
import numpy as np


multiplier, Si_num = 0.1, 84
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





def test_speed_rt(c_wafer,num_particles=100, do_plot=True):
    params = generate_particles(num_particles, c_wafer.xsize,y_ar_plus=y_ar_plus, y_cl=y_cl, y_cl_plus=y_cl_plus, T_i=T_i, T_e=U_i, y0=c_wafer.y0)
    Times1 = []
    Times2 = []
    if do_plot:
        ax = plot_wafer(c_wafer)
    for params_arr in params:
        #print(params_arr)
        if y_cl_plus == 0.0:
            R = 1000
        else:
            R = y_cl / y_cl_plus
        t1 = time.time_ns()
        returned_particles, arr_x, arr_y, rarr_x, rarr_y = process_particles(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.border_arr, [params_arr], c_wafer.Si_num,
            c_wafer.xsize, c_wafer.ysize, R,True, c_wafer.is_half)
        t2 = time.time_ns()
        Times1.append(t2-t1)
        t1 = time.time_ns()
        returned_particles, arr1_x, arr1_y, rarr_x, rarr_y = p_p_old(
            c_wafer.counter_arr, c_wafer.is_full, c_wafer.border_arr, [params_arr], c_wafer.Si_num,
            c_wafer.xsize, c_wafer.ysize, R, True, c_wafer.is_half)
        t2 = time.time_ns()
        Times2.append(t2 - t1)

        if do_plot:
            ax.plot(arr_x, arr_y,color="r")
    Times1 = np.array(Times1)[1:]
    Times2 = np.array(Times2)[1:]
    print('Вpемя новое: ' + str(round(np.mean(Times1[1:])*0.001, 1)) + " +- " + str(round(np.std(Times1[1:])*0.001, 1)))
    print('Вpемя старое: ' + str(round(np.mean(Times2[1:])*0.001, 1)) + " +- " + str(round(np.std(Times2[1:])*0.001, 1)))
    #plt.hist(Times1, label="Новое время", bins=10, range=[Times1.max()*0.5,Times1.max()])
    #plt.hist(Times2, label="Старое время", bins=10, range=[Times1.max()*0.5,Times2.max()])
    #plt.legend()
    #plt.show()
    if do_plot:
        plt.show()

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
X, Y = del_some_structure(rt_wafer,10000, seed=12)
rt_wafer.check_correction()
t3 = time.time()
#X, Y = give_line_arrays(rt_wafer.border_arr)
#f = generate_figure(rt_wafer, wafer_curr_type="is_cell", do_plot_line=True)
#plt.show()

test_speed_rt(rt_wafer,num_particles=100, do_plot=True)


#plt.show()