import numpy as np
from res.getero.algorithm.main_cycle import process_particles
from res.getero.algorithm.monte_carlo import generate_particles
import time
from tqdm import trange
from res.getero.algorithm.dynamic_profile import give_line_arrays, give_max_y
from res.getero.frontend.grafic_funcs import plot_animation
from res.getero.algorithm.dynamic_profile import delete_point, create_point


class WaferGenerator:
    def __init__(self, master, multiplier, Si_num):
        self.master = master
        generate_pure_wafer(self, multiplier, Si_num)
        X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1, 1,
                                size=1)
        self.profiles = []
        self.profiles.append([X, Y])

    def change_plasma_params(self, params):
        n_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

        self.y_ar_plus = params["j_ar_plus"]/n_full
        self.y_cl = params["j_cl"]/n_full
        self.y_cl_plus = params["j_cl_plus"]/n_full
        self.cell_size = params["cell_size"]

        self.N = n_full*self.xsize*self.cell_size*params["a_0"]
        #print(self.N)
        print(str(self.silicon_size*self.cell_size*(10**10))+" angstrem")

        self.T_i = params["T_i"]
        self.U_i = params["U_i"]

    def run(self, num_iter, num_per_iter):
        ftime = (num_iter*num_per_iter)/self.N
        print("Full time: ", str(ftime)+" s.")
        self.master.contPanel.progress_bar["maximum"] = num_iter
        self.old_wif = self.is_full.copy()
        self.old_wca = self.counter_arr.copy()
        self.master.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        for i in trange(num_iter):

            t1 = time.time()
            params = generate_particles(num_per_iter, self.xsize, y_ar_plus=self.y_ar_plus, y_cl=self.y_cl,
                                        y_cl_plus=self.y_cl_plus, T_i=self.T_i, T_e=self.U_i, y0=self.y0)
            t2 = time.time()
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus
            res = process_particles(self.counter_arr, self.is_full, self.border_arr, params, self.Si_num, self.xsize,
                              self.ysize, R, test=False)
            #if res is None:
            #    pass
            #else:
            #    np.save("curr_counter_arr.npy",res)
            #    int("fffdf")
            if i % 10 == 0:
                X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1.5, 1.5,
                                        size=1)
                self.profiles.append([X, Y])
            if i % 1000 == 0:
                print("Num iter: "+str(i)+" Time: "+str(round(ftime*((i+1)/num_iter),3)))
                y_max = give_max_y(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y)
                y_0 = self.border + self.mask_height

                depth = (y_max-y_0) * self.cell_size * (10 ** 10)
                print("Depth: ", depth, " angstrem")
                print("Speed: "+str(round((60*depth/ftime)))+" angstrem/min")
                self.master.plotF.replot(i, False)
                self.master.plotF.f.savefig("files/tmp_U"+str(round(self.U_i,1))+"_"+str(i)+".png")
                #self.master.plotF.send_picture()
            t3 = time.time()

            self.master.contPanel.progress_var.set(i + 1)
            self.master.contPanel.progress_bar.update()
            self.master.style.configure("LabeledProgressbar", text=str(i + 2) + "/" + str(num_iter))
        #self.master.plotF.replot(i)
        self.master.plotF.f.savefig("files/tmp" + "_end" + ".png")
        self.master.style.configure("LabeledProgressbar", text="0/0")
        self.master.contPanel.progress_var.set(0)


def generate_pure_wafer(object, multiplier, Si_num, fill_sicl3=False):
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



def clear_between_mask(object):
    for i in range(object.right_area - object.left_area):
        for j in range(object.mask_height):
            delete_point(object.border_arr, i+object.left_area, j+object.border)
            object.counter_arr[:, i+object.left_area, j+object.border] = np.array([0, 0, 0, 0])
            object.is_full[i+object.left_area, j+object.border] = 0