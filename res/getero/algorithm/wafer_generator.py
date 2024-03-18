import res.config.getero_reactions as config
import numpy as np
from res.getero.algorithm.main_cycle import process_particles
from res.getero.algorithm.monte_carlo import generate_particles
import time
from tqdm import trange

class WaferGenerator:
    def __init__(self, master):
        is_full = np.fromfunction(lambda i, j: j >= config.wafer_border, (config.wafer_xsize, config.wafer_ysize), dtype=int).astype(int)
        counter_arr = is_full.copy() * config.wafer_Si_num
        mask = np.ones((config.wafer_xsize, config.wafer_ysize))
        mask[:, :config.wafer_border] = mask[:, :config.wafer_border] * 0
        mask[:, config.wafer_border + config.wafer_mask_height:config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] = mask[:,
                                                                                                               config.wafer_border + config.wafer_mask_height:config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] * 0
        mask[config.wafer_left_area:config.wafer_right_area, :config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] = mask[
                                                                                                              config.wafer_left_area:config.wafer_right_area,
                                                                                                              :config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] * 0
        config.wafer_is_full = mask + is_full
        config.wafer_counter_arr = np.repeat(counter_arr.reshape(1, counter_arr.shape[0],counter_arr.shape[1]),4,axis=0)
        config.wafer_counter_arr[1] = config.wafer_counter_arr[1] * 0
        config.wafer_counter_arr[2] = config.wafer_counter_arr[2] * 0
        config.wafer_counter_arr[3] = config.wafer_counter_arr[3] * 0

        config.wafer_counter_arr[0] = config.wafer_counter_arr[0] - mask * config.wafer_Si_num
        self.master= master

    def run(self, num_iter, num_per_iter):
        self.master.contPanel.progress_bar["maximum"] = num_iter
        config.old_wif = config.wafer_is_full.copy()
        config.old_wca = config.wafer_counter_arr.copy()
        self.master.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        for i in trange(num_iter):
            #plot_cells(ax, is_full, config.ysize, config.xsize)
            t1 = time.time()
            params = generate_particles(num_per_iter, config.wafer_xsize, y_ar_plus=config.y_ar_plus,
                                        y_cl=config.y_cl, y_cl_plus=config.y_cl_plus, T_i=config.T_i, T_e=config.T_e)
            t2 = time.time()
            process_particles(config.wafer_counter_arr, config.wafer_is_full, params, config.wafer_Si_num, config.wafer_xsize, config.wafer_ysize, config.wafer_y0)
            t3 = time.time()
            self.master.contPanel.progress_var.set(i+1)
            self.master.contPanel.progress_bar.update()
            self.master.style.configure("LabeledProgressbar", text=str(i+2)+"/"+str(num_iter))
        self.master.style.configure("LabeledProgressbar", text="0/0")
        self.master.contPanel.progress_var.set(0)