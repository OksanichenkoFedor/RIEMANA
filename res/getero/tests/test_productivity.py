from res.global_entities.wafer import Wafer
from res.getero.algorithm.ray_tracing_sbs import process_particles
from res.getero.algorithm.monte_carlo import generate_particles

from res.global_entities.plotter import generate_figure

#import res.utils.config as config
from tqdm import trange
import time
import matplotlib.pyplot as plt
import numpy as np

cell_size = 2.5
plasma_params = {
    "T_i": 0.12,
    "U_i": 40,
    "j_ar_plus": 2.041839429440525e+19,
    "j_cl_plus": 1.4431736576424567e+20,
    "j_cl": 2.6629180745936804e+22,
    "cell_size": cell_size*(10.0**(-9)),
    "time": 50,
    "a_0": (((1839*28*9.1*10**(-31))/2330)**(1.0/3.0)) #размер одного слоя Si
}
old_start_test_time, old_end_test_time = 9.977, 12.148
old_start_fast_time, old_end_fast_time = 8.188, 10.556
old_start_test_dob_time, old_end_test_dob_time = 15.084, 21.327

print("Тестовый режим (без добавления): ", round(old_start_test_time, 3), " ", round(old_end_test_time, 3))
print("Тестовый режим (c добавлением): ", round(old_start_test_dob_time, 3), " ", round(old_end_test_dob_time, 3))
print("Самый ускореный результат: ", round(old_start_fast_time, 3), " ", round(old_end_fast_time, 3))


def count_time(curr_wafer, num_iter, num_per_iter, num_mean=250, test=False):
    params = plasma_params
    n_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

    y_ar_plus = params["j_ar_plus"]/n_full
    y_cl = params["j_cl"]/n_full
    y_cl_plus = params["j_cl_plus"]/n_full
    cell_size = params["cell_size"]
    #print(y_cl, y_ar_plus, y_cl_plus)

    #N = n_full*wafer.xsize*cell_size*params["a_0"]

    T_i = params["T_i"]
    U_i = params["U_i"]

    curr_wafer.old_wif = curr_wafer.is_full.copy()
    curr_wafer.old_wca = curr_wafer.counter_arr.copy()
    start_t = time.time()
    Times = []

    for i in trange(num_iter):
        t1 = time.time()
        curr_num_per_iter = num_per_iter
        if curr_wafer.is_half:
            curr_num_per_iter = int(0.5 * curr_num_per_iter)
        params = generate_particles(curr_num_per_iter, curr_wafer.xsize, y_ar_plus=y_ar_plus, y_cl=y_cl,
                                y_cl_plus=y_cl_plus, T_i=T_i, T_e=U_i, y0=curr_wafer.y0)

        if y_cl_plus == 0.0:
            R = 1000
        else:
            R = y_cl / y_cl_plus
        res, _, _, _, _ = process_particles(curr_wafer.counter_arr, curr_wafer.is_full, curr_wafer.border_arr, params,
                                        curr_wafer.Si_num, curr_wafer.xsize,
                                        curr_wafer.ysize, R, test=test, do_half=curr_wafer.is_half)
        t2 = time.time()
        if i!=0:
            Times.append(t2-t1)
    end_t = time.time()
    np_time = np.array(Times)[5:-5]
    middle_time = np_time.mean()
    mid_time = np.zeros(np_time.shape[0]-num_mean+1)
    for i in range(num_mean):
        #print(i, " : ", np_time[i:np_time.shape[0]-num_mean+1+i].shape)
        mid_time = mid_time+np_time[i:np_time.shape[0]-num_mean+1+i]
    mid_time = mid_time/(1.0*num_mean)
    return mid_time, middle_time

#num_iter = 10000
num_iter = 2000
num_per_iter = 2000
num_mean = 500
multiplier, Si_num = 0.05, 84

test_productivity_pure_wafer_params = {
    "mask_height": 200,
    "hole_size": 200,
    "border": 500,
    "xsize": 1000,
    "ysize": 2400,
    "silicon_size": 1600
}

start_wafer = Wafer()
start_wafer.generate_pure_wafer(multiplier, Si_num, params=test_productivity_pure_wafer_params)

start_mid_time, start_middle_time = count_time(start_wafer, num_iter=num_iter,
                                               num_per_iter=num_per_iter, num_mean=num_mean, test=False)
print("Быстрое время в начале: ", round(1000*start_middle_time, 3), " мс")

f = generate_figure(start_wafer, wafer_curr_type="is_cell", do_plot_line=True)


start_wafer = Wafer()
start_wafer.generate_pure_wafer(multiplier, Si_num, params=test_productivity_pure_wafer_params)
start_wafer.make_half()

_, start_middle_time = count_time(start_wafer, num_iter=num_iter,
                                               num_per_iter=num_per_iter, num_mean=num_mean, test=False)
print("Быстрое время в начале половинка: ", round(1000*start_middle_time, 3), " мс")

start_wafer.return_half()
f = generate_figure(start_wafer, wafer_curr_type="is_cell", do_plot_line=True)

plt.show()

start_test_wafer = Wafer()
start_test_wafer.generate_pure_wafer(multiplier, Si_num, params=test_productivity_pure_wafer_params)

start_test_mid_time, start_test_middle_time = count_time(start_test_wafer, num_iter=num_iter,
                                               num_per_iter=num_per_iter, num_mean=num_mean, test=True)
print("Тестировочное время в начале: ", round(1000*start_test_middle_time, 3), " мс")

end_wafer = Wafer()
end_wafer.load("files/test_wafer_16000.zip")

end_mid_time, end_middle_time = count_time(end_wafer, num_iter=num_iter,
                                               num_per_iter=num_per_iter, num_mean=num_mean, test=False)
print("Быстрое время в конце: ", round(1000*end_middle_time, 3), " мс")

end_test_wafer = Wafer()
end_test_wafer.load("files/test_wafer_16000.zip")

end_test_mid_time, end_test_middle_time = count_time(end_test_wafer, num_iter=num_iter,
                                               num_per_iter=num_per_iter, num_mean=num_mean, test=True)
print("Тестировочное время в конце: ", round(1000*end_test_middle_time, 3), " мс")


plt.plot(start_mid_time*1000.0, label="Start time")
plt.plot(end_mid_time*1000.0, label="End time")
plt.plot(start_test_mid_time*1000.0, label="Start test time")
plt.plot(end_test_mid_time*1000.0, label="End test time")
plt.legend()
plt.grid()
plt.xlabel("Номер итерации")
plt.ylabel("Время на одну итерацию, мс")
plt.show()