import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib
from tkinter.ttk import Frame, Style

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

import res.config.getero_reactions as config
from res.getero.frontend.grafic_funcs import plot_cells
from res.getero.algorithm.space_orientation import find_prev
from res.getero.tests.test_geom.test_main_cycle import test_process_particles, process_particles

from res.getero.algorithm.types_of_particle import types


class TestPlotFrame(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.f = Figure(figsize=(9, 9), dpi=100, tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)
        self.canvas.mpl_connect('key_press_event', self.click_keyboard)
        self.generate_field()
        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.ax = self.f.add_subplot(1, 1, 1)

        self.found = 0
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.clicked = False

        self.plot()


    def generate_field(self):
        multiplier = 0.005
        wafer_Si_num = 1
        wafer_border = int(500 * multiplier)
        wafer_xsize = int(2000 * multiplier)
        config.wafer_xsize = wafer_xsize
        wafer_ysize = int(1800 * multiplier)
        config.wafer_ysize = wafer_ysize
        wafer_left_area = int(800 * multiplier)
        wafer_right_area = int(1200 * multiplier)
        wafer_mask_height = int(100 * multiplier)
        wafer_y0 = 0
        wafer_silicon_size = int(800 * multiplier)

        is_full = np.fromfunction(lambda i, j: j >= wafer_border, (wafer_xsize, wafer_ysize),
                                  dtype=int).astype(int)
        counter_arr = is_full.copy() * wafer_Si_num
        mask = np.ones((wafer_xsize, wafer_ysize))
        mask[:, :wafer_border] = mask[:, :wafer_border] * 0
        mask[:,
        wafer_border + wafer_mask_height:wafer_border + wafer_mask_height + wafer_silicon_size] = mask[:, wafer_border + wafer_mask_height:wafer_border + wafer_mask_height + wafer_silicon_size] * 0
        mask[wafer_left_area:wafer_right_area,:wafer_border + wafer_mask_height + wafer_silicon_size] = mask[
                                                                                       wafer_left_area:wafer_right_area,
                                                                                       :wafer_border + wafer_mask_height + wafer_silicon_size] * 0
        config.wafer_is_full = mask + is_full
        config.wafer_counter_arr = np.repeat(counter_arr.reshape(1, counter_arr.shape[0], counter_arr.shape[1]), 4,
                                             axis=0)
        config.wafer_counter_arr[1] = config.wafer_counter_arr[1] * 0
        config.wafer_counter_arr[2] = config.wafer_counter_arr[2] * 0
        config.wafer_counter_arr[3] = config.wafer_counter_arr[3] * 0
        config.wafer_Si_num = wafer_Si_num

        config.wafer_counter_arr[0] = config.wafer_counter_arr[0] - mask * config.wafer_Si_num
    def plot(self):
        self.replot()

    def replot(self):
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        #self.ax.plot([1,2,3],[1,2,3])
        curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(self.ax, config.wafer_counter_arr, config.wafer_is_full,
                   config.wafer_ysize, config.wafer_xsize, curr_type, True, config.test_x, config.test_y)
        if self.found == 1:
            circle1 = plt.Circle((self.x1-0.5, self.y1-0.5), 0.2, color='r')
            self.ax.add_patch(circle1)
        elif self.found == 2:
            self.ax.arrow(self.x1-0.5, self.y1-0.5, 5 * np.sin(self.angle), 5 * np.cos(self.angle), color="g", linewidth=1)
        self.ax.grid(True)
        self.canvas.draw()

    def count_angle(self):
        delta_x = self.x2 - self.x1
        delta_y = self.y2 - self.y1
        delta = np.sqrt(delta_x**2 + delta_y**2)
        if delta_x > 0:
            if delta_y >= 0:
                # первая четверть
                self.angle = np.arctan(delta_x/delta_y)
            else:
                # вторая четверть
                self.angle = np.pi - np.arctan((-1.0)*(delta_x/delta_y))
        else:
            if delta_y >= 0:
                # четвёртая четверть
                self.angle = 2.0*np.pi - np.arctan((-1.0)*(delta_x/delta_y))
            else:
                # третья четверть
                self.angle = np.pi + np.arctan(delta_x/delta_y)


    def move_mouse_event(self, event):
        #print(event)
        pass

    def click_mouse_event(self, event):
        if self.clicked:
            return 0
        self.clicked = True
        if self.found==0:
            self.x1 = event.xdata+0.5
            self.y1 = int(event.ydata+0.5)
            self.found = 1
            self.replot()
        elif self.found==1:
            self.x2 = event.xdata+0.5
            self.y2 = event.ydata+0.5
            self.found = 2
            self.count_angle()
            self.replot()
        elif self.found==2:
            self.replot()
            curr_en = 0
            params_arr = [[self.x1, curr_en, self.angle, config.test_type]]

            if config.y_cl_plus==0.0:
                R = 1000
            else:
                R = config.y_cl/config.y_cl_plus

            config.wafer_counter_arr, config.wafer_is_full, \
            arr_x, arr_y, rarr_x, rarr_y = process_particles(config.wafer_counter_arr, config.wafer_is_full, params_arr,
                                             config.wafer_Si_num, config.wafer_xsize, config.wafer_ysize,
                                             self.y1, R, config.otn_const)
            self.recheck_cell()
            self.replot()

            self.ax.plot(rarr_x, rarr_y, "o", color="r")
            self.ax.plot(arr_x, arr_y, ".", color="g")

            self.canvas.draw()
            self.found = 0

    def unclick_mouse_event(self, event):
        self.clicked = False

    def click_keyboard(self, event):
        #print('Key pressed:', event.key)
        if event.key == "right":
            #print("1")
            if config.test_x<config.wafer_xsize:
                config.test_x+=1
        elif event.key == "left":
            #print("2")
            if config.test_x>0:
                config.test_x-=1
        elif event.key == "down":
            #print("3")
            if config.test_y<config.wafer_ysize:
                config.test_y+=1
        elif event.key == "up":
            #print("4")
            if config.test_y>0:
                config.test_y-=1
        elif event.key == "d":
            config.wafer_counter_arr[:, config.test_x, config.test_y] = np.array([0,0,0,0])
            config.wafer_is_full[config.test_x, config.test_y] = 0
        else:
            return None


        self.recheck_cell()
        self.replot()

        #print('Modifier keys:', event.modifier)


    def recheck_cell(self):
        self.master.contPanel.si_lbl["text"] = "Si: " + str(config.wafer_counter_arr[0][config.test_x, config.test_y])
        self.master.contPanel.sicl_lbl["text"] = "SiCl: " + str(
            config.wafer_counter_arr[1][config.test_x, config.test_y])
        self.master.contPanel.sicl2_lbl["text"] = "SiCl2: " + str(
            config.wafer_counter_arr[2][config.test_x, config.test_y])
        self.master.contPanel.sicl3_lbl["text"] = "SiCl3: " + str(
            config.wafer_counter_arr[3][config.test_x, config.test_y])
