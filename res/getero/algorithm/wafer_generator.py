import numpy as np
from res.getero.algorithm.main_cycle import process_particles
from res.getero.algorithm.monte_carlo import generate_particles
import time
from tqdm import trange
from res.getero.algorithm.dynamic_profile import give_line_arrays
from res.getero.frontend.grafic_funcs import plot_animation


class WaferGenerator:
    def __init__(self, master, multiplier, Si_num):
        self.master = master
        generate_wafer(self, multiplier, Si_num)
        X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1, 1,
                                size=1)
        self.profiles = []
        self.profiles.append([X, Y])

    def change_plasma_params(self, params):
        self.y_ar_plus = params["y_ar_plus"]
        self.y_cl = params["y_cl"]
        self.y_cl_plus = params["y_cl_plus"]
        self.T_i = params["T_i"]
        self.T_e = params["T_e"]

    def run(self, num_iter, num_per_iter):
        self.master.contPanel.progress_bar["maximum"] = num_iter
        self.old_wif = self.is_full.copy()
        self.old_wca = self.counter_arr.copy()
        self.master.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        for i in range(num_iter):

            t1 = time.time()
            params = generate_particles(num_per_iter, self.xsize, y_ar_plus=self.y_ar_plus, y_cl=self.y_cl,
                                        y_cl_plus=self.y_cl_plus, T_i=self.T_i, T_e=self.T_e, y0=self.y0)
            t2 = time.time()
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus
            process_particles(self.counter_arr, self.is_full, self.border_arr, params, self.Si_num, self.xsize,
                              self.ysize, R, test=False)
            if i % 10 == 0:
                X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1.5, 1.5,
                                        size=1)
                self.profiles.append([X, Y])
            if i % 500 == 0 and i!=0:
                self.master.plotF.replot(i)
                self.master.plotF.f.savefig("files/tmp"+str(i)+".png")
                #self.master.plotF.send_picture()
            t3 = time.time()

            self.master.contPanel.progress_var.set(i + 1)
            self.master.contPanel.progress_bar.update()
            self.master.style.configure("LabeledProgressbar", text=str(i + 2) + "/" + str(num_iter))
        #self.master.plotF.replot(i)
        self.master.plotF.f.savefig("files/tmp" + "_end" + ".png")
        self.master.style.configure("LabeledProgressbar", text="0/0")
        self.master.contPanel.progress_var.set(0)


def generate_wafer(object, multiplier, Si_num, fill_sicl3=False):
    object.multiplier = multiplier
    object.Si_num = Si_num
    object.border = int(500 * object.multiplier)
    object.xsize = int(2000 * object.multiplier)
    object.ysize = int(2400 * object.multiplier)
    object.left_area = int(800 * object.multiplier)
    object.right_area = int(1200 * object.multiplier)
    object.mask_height = int(100 * object.multiplier)
    object.y0 = 0
    object.silicon_size = int(1600 * object.multiplier)

    object.is_full = np.fromfunction(lambda i, j: j >= object.border, (object.xsize, object.ysize), dtype=int).astype(
        int)
    object.counter_arr = object.is_full.copy() * object.Si_num
    object.mask = np.ones((object.xsize, object.ysize))
    object.mask[:, :object.border] = object.mask[:, :object.border] * 0
    object.mask[:,
    object.border + object.mask_height:object.border + object.mask_height + object.silicon_size] = object.mask[:,
                                                                                                   object.border + object.mask_height:object.border +
                                                                                                                                      object.mask_height + object.silicon_size] * 0
    object.mask[object.left_area:object.right_area, :object.border + object.mask_height + object.silicon_size] = \
        object.mask[object.left_area:object.right_area, :object.border + object.mask_height + object.silicon_size] * 0
    object.is_full = object.mask + object.is_full
    object.counter_arr = np.repeat(
        object.counter_arr.reshape(1, object.counter_arr.shape[0], object.counter_arr.shape[1]),
        4, axis=0)
    object.counter_arr[1] = object.counter_arr[1] * 0
    object.counter_arr[2] = object.counter_arr[2] * 0
    ind = 3
    if fill_sicl3:
        ind=0
    object.counter_arr[ind] = object.counter_arr[ind] * 0

    object.counter_arr[0] = object.counter_arr[0] - object.mask * object.Si_num
    object.border_arr = np.ones((object.xsize, object.ysize, 5)) * 0.5
    for i in range(object.xsize):
        object.border_arr[i, object.border, 0] = 1.0
        if i == 0:
            object.border_arr[i, object.border, 1:] = [-1, -1, i + 1, object.border]
            object.start_x, object.start_y = i, object.border
        elif i == object.xsize - 1:
            object.border_arr[i, object.border, 1:] = [i - 1, object.border, -1, -1]
            object.end_x, object.end_y = i, object.border
        else:
            object.border_arr[i, object.border, 1:] = [i - 1, object.border, i + 1, object.border]

    object.border_arr[:, :object.border - 0, :] = object.border_arr[:, :object.border - 0, :] * (
        -2.0)
    object.border_arr[:, object.border + 1:, :] = object.border_arr[:, object.border + 1:, :] * (
        0.0)

    object.border_arr = object.border_arr.astype(int)
    print("---")


import matplotlib.pyplot as plt
import matplotlib.animation as animation



