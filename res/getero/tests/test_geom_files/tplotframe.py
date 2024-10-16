import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib
from tkinter.ttk import Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from res.getero.ray_tracing.bvh.algorithm import build_BVH, bvh_count_collision_point
from res.getero.ray_tracing.profile_approximation import count_norm_angle

matplotlib.use('TkAgg')

import res.utils.config as config
from res.getero.frontend.grafic_funcs import plot_cells, plot_line
from res.getero.algorithm.main_cycle import process_particles

from res.global_entities.wafer import Wafer

from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays, create_point


# from res.getero.algorithm.wafer_generator import generate_pure_wafer


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
        self.wafer = Wafer()
        self.wafer.generate_pure_wafer(0.008, 1, fill_sicl3=True)
        self.wafer.make_half()
        self.wafer.return_half()
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
        self.test_x = 2
        self.test_y = 5
        self.is_collide = False

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
        plot_cells(self.ax, self.wafer, curr_type, True, self.test_x, self.test_y)
        if self.found == 1:
            circle1 = plt.Circle((self.x1 - 0.5, self.y1 - 0.5), 0.2, color='r')
            self.ax.add_patch(circle1)
        elif self.found == 2 and self.is_collide:
            #self.ax.arrow(self.x1 - 0.5, self.y1 - 0.5, 5 * np.sin(self.angle), 5 * np.cos(self.angle), color="g",
            #              linewidth=1)
            self.ax.plot([self.curr_vec[0]-0.5, self.coll_vec[0]-0.5], [self.curr_vec[1]-0.5, self.coll_vec[1]-0.5], color=(1, 0, 0, 0.1))
            print(self.bX, self.bY)
            self.ax.plot(self.bX-0.5, self.bY-0.5, ".", color="y")
            self.ax.plot(self.bX - 0.5, self.bY - 0.5, color="y")
            self.ax.plot([self.coll_vec[0]-0.5, self.coll_vec[0]-0.5 + 5 * np.cos(self.n_angle)],
                   [self.coll_vec[1]-0.5, self.coll_vec[1]-0.5 + 5 * np.sin(self.n_angle)], color=(0.5,0,0))
            alpha = 2.0 / (max(np.abs(self.A), np.abs(self.B)))
            x = alpha * np.arange(-1, 1, 0.1) * self.B + self.coll_vec[0] - 0.5
            y = alpha * np.arange(-1, 1, 0.1) * (-1.0 * self.A) + self.coll_vec[1] - 0.5
            self.ax.plot(x, y, color="g")
        X, Y = give_line_arrays(self.wafer.border_arr, self.wafer.is_half)  # 0, 0)
        plot_line(self.ax, X, Y, 0, 0, do_points=False)
        if self.is_collide and False:
            #print("fffffff")
            self.ax.plot([self.x1 - 0.5, self.x_c - 0.5], [self.y1 - 0.5, self.y_c - 0.5], color="k")

        for x in range(self.wafer.border_arr.shape[0]):
            for y in range(self.wafer.border_arr.shape[1]):
                color = "g"
                if self.wafer.border_arr[x, y, 0] == 1:
                    color = (0.5, 0, 0.5)
                curr_str0 = "curr: " + str(int(x)) + "," + str(int(y))
                curr_str1 = "prev: " + str(int(self.wafer.border_arr[x, y, 1])) + "," + str(
                    int(self.wafer.border_arr[x, y, 2]))
                curr_str2 = "next: " + str(int(self.wafer.border_arr[x, y, 3])) + "," + str(
                    int(self.wafer.border_arr[x, y, 4]))
                self.ax.text(x - 0.3, y + 0.4, curr_str0, color=color, fontsize=5)
                self.ax.text(x - 0.3, y + 0.2, curr_str1, color=color, fontsize=5)
                self.ax.text(x - 0.3, y + 0.0, curr_str2, color=color, fontsize=5)
                self.ax.text(x - 0.3, y + 0.2, str(int(self.wafer.border_arr[x, y, 0])), color=color, fontsize=9)
        self.ax.grid(True)
        if not (self.arr_y is None):
            # print("FfFFF: ",self.arr_x, self.arr_y, self.rarr_x, self.rarr_y)
            # self.ax.plot(self.rarr_x, self.rarr_y, "o", color="r")
            # self.ax.plot(self.rarr_x, self.rarr_y, color="r")
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

            curr_en = 0
            # self.test_type = 0
            params_arr = [[self.x1, self.y1, 1, curr_en, self.angle, self.test_type, int(self.x1),
                           self.y1 ]]

            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus
            self.curr_vec = np.zeros(2)
            self.curr_vec[0] = params_arr[0][0]
            self.curr_vec[1] = params_arr[0][1]
            start_segment = np.ones((2, 2)) * (-1.0)
            curr_en = params_arr[0][3]
            self.curr_angle = params_arr[0][4]
            curr_type = params_arr[0][5]
            NodeList = build_BVH(self.wafer.border_arr, self.wafer.is_half)
            self.is_collide, self.coll_vec, norm_angle, start_segment, _ = bvh_count_collision_point(NodeList,
                                                                                                  self.curr_vec,
                                                                                                  self.curr_angle,
                                                                                                  start_segment)
            self.n_angle, deb, self.bX, self.bY, self.A, self.B = count_norm_angle(self.wafer.border_arr, self.coll_vec, start_segment,
                                                                   self.wafer.is_half,
                                                                   num_one_side_points=2)

            self.replot()
        elif self.found == 2:
            self.replot()
            #returned_particles, self.arr_x, self.arr_y, self.rarr_x, self.rarr_y = process_particles(
            #    self.wafer.counter_arr,
            #    self.wafer.is_full, self.wafer.border_arr,
            #    params_arr, self.wafer.Si_num,
            #    self.wafer.xsize, self.wafer.ysize, R,
            #    True, self.wafer.is_half)
            #returned_particles, self.arr_x, self.arr_y, self.rarr_x, self.rarr_y = process_particles(
            #    self.wafer.counter_arr,
            #    self.wafer.is_full, self.wafer.border_arr,
            #    params_arr, self.wafer.Si_num,
            #    self.wafer.xsize, self.wafer.ysize, R,
            #    True, self.wafer.is_half)
            self.recheck_cell()
            #self.replot()

            self.canvas.draw()
            # print("fdfdfdfdfdf1")
            self.found = 0

    def unclick_mouse_event(self, event):
        self.clicked = False

    def click_keyboard(self, event):
        # print('Key pressed:', event.key)
        if event.key == "right":
            # print("1")
            if self.test_x < self.wafer.xsize:
                self.test_x += 1
        elif event.key == "left":
            # print("2")
            if self.test_x > 0:
                self.test_x -= 1
        elif event.key == "down":
            # print("3")
            if self.test_y < self.wafer.ysize:
                self.test_y += 1
        elif event.key == "up":
            # print("4")
            if self.test_y > 0:
                self.test_y -= 1
        elif event.key == "d":
            self.wafer.counter_arr[:, self.test_x, self.test_y] = np.array([0, 0, 0, 0])
            self.wafer.is_full[self.test_x, self.test_y] = 0
            self.wafer.add_segments = delete_point(self.wafer.border_arr, self.wafer.is_full, self.wafer.is_hard, self.wafer.add_segments,
                         self.test_x, self.test_y)
        elif event.key == "c":
            if self.click_mode:
                print("click mode off")
                self.click_mode = False
            else:
                print("click mode on")
                self.click_mode = True
        elif event.key == "r":
            print("reconstruct")
            # self.cursed_params = [[20.740437817923226, 0.0, 1.0, 40.0, 6.248322057011167, 3.0, 20.0, 0.0]]
            # self.cursed_params = [[20.321909235834088, 12.0, 1.0, 19.43, 3.176455903758212, 9.0, 20.0, 11.0]]
            f = open("del5.txt")
            A = f.readlines()
            f.close()
            for line in A[:]:
                line = line.split()
                if len(line) == 3:
                    x = int(line[1])
                    y = int(line[2])
                    self.wafer.counter_arr[:, x, y] = np.array([0, 0, 0, 0])
                    self.wafer.is_full[x, y] = 0
                    self.wafer.add_segments = delete_point(self.wafer.border_arr, self.wafer.is_full,
                                                           self.wafer.is_hard, self.wafer.add_segments,
                                                           self.test_x, self.test_y)
                    # time.sleep(0.05)
                    print("Delete: ", x, y)
                    # self.replot()
                elif len(line) == 6:
                    prev_x = int(line[1])
                    prev_y = int(line[2])
                    curr_x = int(line[4])
                    curr_y = int(line[5])
                    self.wafer.counter_arr[:, prev_x, prev_y] = np.array([0, 0, 0, 1])
                    self.wafer.is_full[prev_x, prev_y] = 1
                    create_point(self.wafer.border_arr, self.wafer.is_full, prev_x, prev_y, curr_x, curr_y)
                    print("Create: ", prev_x, prev_y, " from: ", curr_x, curr_y)
            self.replot()
            # self.ax.plot(self.cursed_params[0][0], self.cursed_params[0][1], ".", color=(0.5, 0.7, 0.3))
            # print("angle: ", self.cursed_params[0][4] / np.pi)
            self.canvas.draw()
            return None
        elif event.key == "p":
            print("start cursed reaction")
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus

            self.arr_x, self.arr_y, self.rarr_x, self.rarr_y, returned_particles = process_particles(
                self.wafer.counter_arr, self.is_full,
                self.wafer.border_arr, self.cursed_params,
                self.wafer.Si_num,
                self.wafer.xsize, self.wafer.ysize, R, True,
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
            curr_len = len(A) // 4
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
                rect = plt.Rectangle((c_a_x[i] - 0.5, c_a_y[i] - 0.5), 1, 1, color="g")
                self.ax.add_patch(rect)
            self.ax.plot(np.array(Curr_x) - 0.5, np.array(Curr_y) - 0.5, ".", color="b")
            self.ax.plot(np.array(Curr_x) - 0.5, np.array(Curr_y) - 0.5, color="b")
            self.canvas.draw()
        elif event.key == "g":
            # меняем тип частицы
            if self.test_type == 0:
                print("Меняем тип на создание")
                self.test_type = 4
            elif self.test_type == 4:
                print("Меняем тип на удаление")
                self.test_type = 0
        else:
            return None

        self.recheck_cell()
        self.replot()

        # print('Modifier keys:', event.modifier)

    def recheck_cell(self):
        self.master.contPanel.si_lbl["text"] = "Si: " + str(self.wafer.counter_arr[0][self.test_x, self.test_y])
        self.master.contPanel.sicl_lbl["text"] = "SiCl: " + str(
            self.wafer.counter_arr[1][self.test_x, self.test_y])
        self.master.contPanel.sicl2_lbl["text"] = "SiCl2: " + str(
            self.wafer.counter_arr[2][self.test_x, self.test_y])
        self.master.contPanel.sicl3_lbl["text"] = "SiCl3: " + str(
            self.wafer.counter_arr[3][self.test_x, self.test_y])