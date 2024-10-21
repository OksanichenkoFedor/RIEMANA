from tqdm import trange
import time
import numpy as np

from res.getero.algorithm.monte_carlo import generate_particles
from res.getero.algorithm.dynamic_profile import give_line_arrays, give_max_y
from res.getero.algorithm.main_cycle import process_particles
from res.getero.ray_tracing.bvh.algorithm import build_BVH
from res.bot.simple import print_message, throw_plot

from res.global_entities.plotter import generate_figure
from res.getero.frontend.grafic_funcs import plot_animation

class Getero:
    def __init__(self):
        self.times = []
        self.depths = []

    def change_plasma_params(self, params):
        #params["j_ar_plus"] = 0
        #params["j_cl_plus"] = 0
        #params["j_cl"] = 0
        self.j_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

        self.y_ar_plus = params["j_ar_plus"]/self.j_full
        self.y_cl = params["j_cl"]/self.j_full
        self.y_cl_plus = params["j_cl_plus"]/self.j_full
        self.cell_size = params["cell_size"]
        self.a_0 = params["a_0"]

        self.T_i = params["T_i"]
        self.U_i = params["U_i"]
        self.y_ar = params["y_ar"]

        self.type_ray_tracing = params["rt_type"]
        self.num_one_side_points = params["num_one_side_points"]

    def run(self, wafer, ctime, num_iter, iter_add_profile=50, iter_save_replot=3000, do_print=True, wafer_curr_type="is_cell", start_filename="", do_half=False):
        self.N_per_sec = self.j_full * wafer.xsize * self.cell_size * self.a_0 * ((1.0*wafer.Si_num)/84.0)
        num_per_iter = int((ctime*self.N_per_sec)/num_iter)
        is_half = wafer.is_half
        print("Full time: ", str(round(ctime, 1)) + " s.")
        print("Number particles per iteration: ", str(num_per_iter))
        #if not (frontender is None):
        #    frontender.progress_bar["maximum"] = num_iter
        #    frontender.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        wafer.old_wif = wafer.is_full.copy()
        wafer.old_wca = wafer.counter_arr.copy()
        Times = []
        Depths = []
        NodeList = build_BVH(wafer.border_arr, wafer.is_half)
        for i in trange(num_iter):

            t1 = time.time()
            curr_num_per_iter = num_per_iter
            params = generate_particles(curr_num_per_iter, wafer.xsize, y_ar_plus=self.y_ar_plus, y_cl=self.y_cl,
                                        y_cl_plus=self.y_cl_plus, T_i=self.T_i, T_e=self.U_i, y0=wafer.y0)
            t2 = time.time()
            if self.y_cl_plus == 0.0:
                R = 1000.0
            else:
                R = float(self.y_cl / self.y_cl_plus)
            res, _, _, _, _, NodeList, wafer.add_segments = process_particles(wafer.counter_arr, wafer.is_full,
                                   wafer.is_hard, wafer.add_segments, wafer.border_arr, params,
                                   wafer.Si_num, wafer.xsize, wafer.ysize, R, test=False, do_half=wafer.is_half,
                                                          NodeList=NodeList, type=self.type_ray_tracing,
                                                          num_one_side_points=self.num_one_side_points)
            if i % iter_add_profile == 0 and i!=0:
                if is_half:
                    wafer.return_half()
                X, Y = give_line_arrays(wafer.border_arr, wafer.is_half)
                wafer.profiles.append([X, Y])
                curr_fig = generate_figure(wafer, wafer_curr_type, do_plot_line=False)
                add_name = "U" + str(round(self.U_i, 1)) + "_Ar" + str(self.y_ar) + "_SiNum" + str(wafer.Si_num)
                c_filename = start_filename + "data/pictures/tmp_" + add_name + "_" + str(i)
                curr_fig.savefig(c_filename + ".png")
                if is_half:
                    wafer.make_half()
            if i % 100 == 0:
                Times.append(ctime * ((i + 1) / num_iter))

                y_max = give_max_y(wafer.border_arr)
                y_0 = wafer.border + wafer.mask_height

                depth = (y_max - y_0) * self.cell_size * (10 ** 10)

                Depths.append(depth)
            if i % iter_save_replot == 0 and i!=0:
                if is_half:
                    add_name = "U" + str(round(self.U_i, 1)) + "_Ar" + str(self.y_ar) + "_SiNum" + str(wafer.Si_num)
                    curr_fig = generate_figure(wafer, wafer_curr_type, do_plot_line=False)
                    c_filename = start_filename + "data/pictures/tmp_f_" + add_name + "_" + str(i)
                    curr_fig.savefig(c_filename + ".png")
                    throw_plot(c_filename + ".png", 710672679)
                    wafer.return_half()
                print("Num iter: " + str(i) + " Time: " + str(round(ctime * ((i + 1) / num_iter), 3)))

                print_message("Num iter: " + str(i) + " Time: " + str(round(ctime * ((i + 1) / num_iter), 3)), 710672679)
                y_max = give_max_y(wafer.border_arr)
                y_0 = wafer.border + wafer.mask_height

                depth = (y_max - y_0) * self.cell_size * (10 ** 10)
                curr_time = ctime * ((i + 1) / num_iter)
                self.depths.append(depth)
                self.times.append(curr_time)
                print("Depth: ", depth, " angstrem")

                print("Speed: " + str(round((60 * depth / curr_time))) + " angstrem/min")
                print_message("Depth: "+str(depth)+" angstrem", 710672679)
                print_message("Speed: " + str(round((60 * depth / curr_time))) + " angstrem/min", 710672679)
                add_name = "U"+str(round(self.U_i, 1)) + "_Ar" + str(self.y_ar) + "_SiNum" + str(wafer.Si_num)
                np.save(start_filename+"data/times" + add_name +".npy", np.array(Times))
                throw_plot(start_filename+"data/times" + add_name +".npy", 710672679)
                np.save(start_filename+"data/depths" + add_name +".npy", np.array(Depths))
                throw_plot(start_filename+"data/depths" + add_name + ".npy", 710672679)
                curr_fig = generate_figure(wafer, wafer_curr_type, do_plot_line=False)
                c_filename = start_filename+"data/pictures/tmp_" + add_name + "_" + str(i)
                curr_fig.savefig(c_filename + ".png")
                plot_animation(wafer.profiles, wafer.xsize, wafer.ysize, 0, filename=c_filename)
                throw_plot(c_filename + ".png", 710672679)
                throw_plot(c_filename + ".gif", 710672679)


                wafer.save(start_filename+"data/wafer_" + add_name + ".zip")

                if is_half:
                    wafer.make_half()
            t3 = time.time()
            #print(t3-t2,t2-t1)