import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib
from tkinter.ttk import Frame, Style
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

import res.utils.config as config
from res.getero.frontend.grafic_funcs import plot_cells, plot_line
from res.getero.algorithm.main_cycle import process_particles

from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays, create_point

from res.getero.algorithm.wafer_generator import generate_pure_wafer


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
        generate_pure_wafer(self, 0.005, 5, fill_sicl3=True)
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
        self.test_x = 5
        self.test_y = 5

        self.y_cl_plus = 0.1
        self.y_cl = 0.8

        self.test_type = 0

        self.arr_x, self.arr_y, self.rarr_x, self.rarr_y = None, None, None, None

        self.click_mode = False

        self.plot()

    def plot(self):
        self.replot()

    def replot(self):
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        # self.ax.plot([1,2,3],[1,2,3])
        curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(self.ax, self.counter_arr, self.is_full,
                   self.ysize, self.xsize, curr_type, True, self.test_x, self.test_y)
        if self.found == 1:
            circle1 = plt.Circle((self.x1 - 0.5, self.y1 - 0.5), 0.2, color='r')
            self.ax.add_patch(circle1)
        elif self.found == 2 and False:
            self.ax.arrow(self.x1 - 0.5, self.y1 - 0.5, 5 * np.sin(self.angle), 5 * np.cos(self.angle), color="g",
                          linewidth=1)
        X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 0,
                                0)
        plot_line(self.ax, X, Y, self.start_x, self.start_y, 0, 0, do_points=False)

        for x in range(self.border_arr.shape[0]):
            for y in range(self.border_arr.shape[1]):
                color = "g"
                if self.border_arr[x, y, 0] == 1:
                    color = (0.5, 0, 0.5)
                curr_str0 = "curr: " + str(int(x)) + "," + str(int(y))
                curr_str1 = "prev: " + str(int(self.border_arr[x, y, 1])) + "," + str(int(self.border_arr[x, y, 2]))
                curr_str2 = "next: " + str(int(self.border_arr[x, y, 3])) + "," + str(int(self.border_arr[x, y, 4]))
                # self.ax.text(x - 0.3, y + 0.4, curr_str0, color=color, fontsize=5)
                # self.ax.text(x - 0.3, y + 0.2, curr_str1, color=color, fontsize=5)
                # self.ax.text(x - 0.3, y + 0.0, curr_str2, color=color, fontsize=5)
                # self.ax.text(x - 0.3, y + 0.2, str(int(self.border_arr[x, y, 0])), color=color, fontsize=9)
        self.ax.grid(True)
        if not (self.arr_y is None):
            # print("FfFFF: ",self.arr_x, self.arr_y, self.rarr_x, self.rarr_y)
            #self.ax.plot(self.rarr_x, self.rarr_y, "o", color="r")
            #self.ax.plot(self.rarr_x, self.rarr_y, color="r")
            self.ax.plot(self.arr_x, self.arr_y, ".", color="g")
            self.ax.plot(self.arr_x, self.arr_y, color="g", alpha=0.3)
        self.canvas.draw()

    def count_angle(self):
        delta_x = self.x2 - self.x1
        delta_y = self.y2 - self.y1
        delta = np.sqrt(delta_x ** 2 + delta_y ** 2)
        if delta_x > 0:
            if delta_y >= 0:
                # первая четверть
                self.angle = np.arctan(delta_x / delta_y)
            else:
                # вторая четверть
                self.angle = np.pi - np.arctan((-1.0) * (delta_x / delta_y))
        else:
            if delta_y >= 0:
                # четвёртая четверть
                self.angle = 2.0 * np.pi - np.arctan((-1.0) * (delta_x / delta_y))
            else:
                # третья четверть
                self.angle = np.pi + np.arctan(delta_x / delta_y)

    def move_mouse_event(self, event):
        # print(event)
        pass

    def click_mouse_event(self, event):
        if not self.click_mode:
            print("Coords: ", round(event.xdata + 0.5, 2), round(event.ydata + 0.5, 2))
            return 0
        if self.clicked:
            return 0
        self.clicked = True
        if self.found == 0:
            self.x1 = event.xdata + 0.5
            self.y1 = int(event.ydata + 0.5)
            self.found = 1
            self.replot()
        elif self.found == 1:
            self.x2 = event.xdata + 0.5
            self.y2 = event.ydata + 0.5
            self.found = 2
            self.count_angle()
            self.replot()
        elif self.found == 2:
            self.replot()
            curr_en = 40
            self.test_type = 3
            params_arr = [[self.x1, self.y1, 1, curr_en, self.angle, self.test_type, int(self.x1), self.y1]]

            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus

            self.arr_x, self.arr_y, self.rarr_x, self.rarr_y, returned_particlesc = process_particles(self.counter_arr,
                                                                                 self.is_full, self.border_arr,
                                                                                 params_arr, self.Si_num,
                                                                                 self.xsize, self.ysize, R, self)
            self.recheck_cell()
            self.replot()

            self.canvas.draw()
            self.found = 0

    def unclick_mouse_event(self, event):
        self.clicked = False

    def click_keyboard(self, event):
        # print('Key pressed:', event.key)
        if event.key == "right":
            # print("1")
            if self.test_x < self.xsize:
                self.test_x += 1
        elif event.key == "left":
            # print("2")
            if self.test_x > 0:
                self.test_x -= 1
        elif event.key == "down":
            # print("3")
            if self.test_y < self.ysize:
                self.test_y += 1
        elif event.key == "up":
            # print("4")
            if self.test_y > 0:
                self.test_y -= 1
        elif event.key == "d":
            self.counter_arr[:, self.test_x, self.test_y] = np.array([0, 0, 0, 0])
            self.is_full[self.test_x, self.test_y] = 0
            delete_point(self.border_arr, self.test_x, self.test_y)
        elif event.key == "c":
            if self.click_mode:
                print("click mode off")
                self.click_mode = False
            else:
                print("click mode on")
                self.click_mode = True
        elif event.key == "r":
            print("reconstruct")
            #self.cursed_params = [[20.740437817923226, 0.0, 1.0, 40.0, 6.248322057011167, 3.0, 20.0, 0.0]]
            #self.cursed_params = [[20.321909235834088, 12.0, 1.0, 19.43, 3.176455903758212, 9.0, 20.0, 11.0]]
            f = open("del5.txt")
            A = f.readlines()
            f.close()
            for line in A[:]:
                line = line.split()
                if len(line) == 3:
                    x = int(line[1])
                    y = int(line[2])
                    self.counter_arr[:, x, y] = np.array([0, 0, 0, 0])
                    self.is_full[x, y] = 0
                    delete_point(self.border_arr, x, y)
                    # time.sleep(0.05)
                    print("Delete: ", x, y)
                    # self.replot()
                elif len(line) == 6:
                    prev_x = int(line[1])
                    prev_y = int(line[2])
                    curr_x = int(line[4])
                    curr_y = int(line[5])
                    self.counter_arr[:, prev_x, prev_y] = np.array([0, 0, 0, 1])
                    self.is_full[prev_x, prev_y] = 1
                    create_point(self.border_arr, prev_x, prev_y, curr_x, curr_y)
                    print("Create: ", prev_x, prev_y, " from: ", curr_x, curr_y)
            self.replot()
            self.ax.plot(self.cursed_params[0][0], self.cursed_params[0][1], ".", color=(0.5, 0.7, 0.3))
            print("angle: ", self.cursed_params[0][4] / np.pi)
            self.canvas.draw()
            return None
        elif event.key == "p":
            print("start cursed reaction")
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus

            self.arr_x, self.arr_y, self.rarr_x, self.rarr_y, returned_particles = process_particles(self.counter_arr, self.is_full,
                                                                                 self.border_arr, self.cursed_params,
                                                                                 self.Si_num,
                                                                                 self.xsize, self.ysize, R, True,
                                                                                 max_value=40)
            print("end cursed reaction")
            self.recheck_cell()
            self.replot()
        elif event.key == "b":
            f = open("path1.txt")
            A = f.readlines()
            f.close()
            Prev_x, Prev_y = [], []
            Curr_x, Curr_y = [], []
            p_a_x, p_a_y = [], []
            c_a_x, c_a_y = [], []
            ifa_p, ifa_c = [], []
            curr_len = len(A)//4
            for i in range(curr_len):
                Prev_x.append(float(A[4 * i + 1].split()[0]))
                Prev_y.append(float(A[4 * i + 1].split()[1]))
                p_a_x.append(float(A[4 * i + 1].split()[2]))
                p_a_y.append(float(A[4 * i + 1].split()[3]))
                Curr_x.append(float(A[4 * i + 2].split()[0]))
                Curr_y.append(float(A[4 * i + 2].split()[1]))
                c_a_x.append(float(A[4 * i + 2].split()[2]))
                c_a_y.append(float(A[4 * i + 2].split()[3]))
                ifa_p.append(float(A[4 * i + 3].split()[0]))
                ifa_c.append(float(A[4 * i + 3].split()[1]))

            print(Curr_x)
            print(Curr_y)
            self.replot()
            for i in range(curr_len):
                rect = plt.Rectangle((c_a_x[i]-0.5,c_a_y[i]-0.5),1,1,color="g")
                self.ax.add_patch(rect)
            self.ax.plot(np.array(Curr_x)-0.5, np.array(Curr_y)-0.5, ".",color="b")
            self.ax.plot(np.array(Curr_x)-0.5, np.array(Curr_y)-0.5,color="b")
            self.canvas.draw()
        else:
            return None

        self.recheck_cell()
        self.replot()

        # print('Modifier keys:', event.modifier)

    def recheck_cell(self):
        self.master.contPanel.si_lbl["text"] = "Si: " + str(self.counter_arr[0][self.test_x, self.test_y])
        self.master.contPanel.sicl_lbl["text"] = "SiCl: " + str(
            self.counter_arr[1][self.test_x, self.test_y])
        self.master.contPanel.sicl2_lbl["text"] = "SiCl2: " + str(
            self.counter_arr[2][self.test_x, self.test_y])
        self.master.contPanel.sicl3_lbl["text"] = "SiCl3: " + str(
            self.counter_arr[3][self.test_x, self.test_y])
