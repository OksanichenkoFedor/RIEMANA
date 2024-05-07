from tqdm import trange
import time
import numpy as np

from res.getero.algorithm.monte_carlo import generate_particles
from res.getero.algorithm.dynamic_profile import give_line_arrays, give_max_y
from res.getero.algorithm.main_cycle import process_particles

class Etcher:
    def __init__(self):
        self.times = []
        self.depths = []

    def change_plasma_params(self, params):
        self.j_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

        self.y_ar_plus = params["j_ar_plus"]/self.j_full
        self.y_cl = params["j_cl"]/self.j_full
        self.y_cl_plus = params["j_cl_plus"]/self.j_full
        self.cell_size = params["cell_size"]
        self.a_0 = params["a_0"]

        self.T_i = params["T_i"]
        self.U_i = params["U_i"]

    def run(self, wafer, ctime, frontender, plotter, num_iter, iter_add_profile=500, iter_save_replot=500):
        self.N_per_sec = self.j_full * wafer.xsize * self.cell_size * self.a_0
        num_per_iter = int((ctime*self.N_per_sec)/num_iter)
        print("Full time: ", str(round(ctime,1)) + " s.")
        print("Number particles per iteration: ", str(num_per_iter))
        if not (frontender is None):
            frontender.progress_bar["maximum"] = num_iter
            frontender.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        wafer.old_wif = wafer.is_full.copy()
        wafer.old_wca = wafer.counter_arr.copy()
        #print(self.y_ar_plus, self.y_cl, self.y_cl_plus, self.U_i, wafer.y0, wafer.xsize, num_per_iter, self.T_i)
        #print(np.mean(wafer.counter_arr))
        for i in trange(num_iter):

            t1 = time.time()
            params = generate_particles(num_per_iter, wafer.xsize, y_ar_plus=self.y_ar_plus, y_cl=self.y_cl,
                                        y_cl_plus=self.y_cl_plus, T_i=self.T_i, T_e=self.U_i, y0=wafer.y0)
            t2 = time.time()
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus
            res = process_particles(wafer.counter_arr, wafer.is_full, wafer.border_arr, params,
                                    wafer.Si_num, wafer.xsize, wafer.ysize, R, test=False)
            if i % iter_add_profile == 0 and i!=0:
                X, Y = give_line_arrays(wafer.border_arr, wafer.start_x, wafer.start_y, wafer.end_x,
                                        wafer.end_y, 1.5, 1.5)
                wafer.profiles.append([X, Y])
            if i % iter_save_replot == 0:
                print("Num iter: " + str(i) + " Time: " + str(round(ctime * ((i + 1) / num_iter), 3)))
                y_max = give_max_y(wafer.border_arr, wafer.start_x, wafer.start_y, wafer.end_x, wafer.end_y)
                y_0 = wafer.border + wafer.mask_height

                depth = (y_max - y_0) * self.cell_size * (10 ** 10)
                curr_time = ctime * ((i + 1) / num_iter)
                self.depths.append(depth)
                self.times.append(curr_time)
                print("Depth: ", depth, " angstrem")
                print("Speed: " + str(round((60 * depth / curr_time))) + " angstrem/min")
                if not (frontender is None):
                    plotter.replot(wafer, i, False)
                    plotter.f.savefig("data/pictures/tmp_U" + str(round(self.U_i, 1)) + "_" + str(i) + ".png")
                    # self.master.plotF.send_picture()
                wafer.save("data/test.zip")
                    #self.wafer.load("test.zip")
            t3 = time.time()
            if not (frontender is None):
                frontender.progress_var.set(i + 1)
                frontender.progress_bar.update()
                frontender.style.configure("LabeledProgressbar", text=str(i + 2) + "/" + str(num_iter))