import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib
from tkinter.ttk import Frame, Style

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

import res.utils.config as config
from res.getero.frontend.grafic_funcs import plot_cells, plot_line
from res.getero.algorithm.main_cycle import process_particles

from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays

from res.getero.algorithm.wafer_generator import generate_wafer


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
        generate_wafer(self, 0.005, 1)
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
        self.test_x = 0
        self.test_y = 0

        self.y_cl_plus = 0.1
        self.y_cl = 0.8

        self.test_type = 0

        self.plot()

    def plot(self):
        self.replot()

    def replot(self):
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        #self.ax.plot([1,2,3],[1,2,3])
        curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(self.ax, self.counter_arr, self.is_full,
                   self.ysize, self.xsize, curr_type, True, self.test_x, self.test_y)
        if self.found == 1:
            circle1 = plt.Circle((self.x1-0.5, self.y1-0.5), 0.2, color='r')
            self.ax.add_patch(circle1)
        elif self.found == 2:
            self.ax.arrow(self.x1-0.5, self.y1-0.5, 5 * np.sin(self.angle), 5 * np.cos(self.angle), color="g", linewidth=1)
        X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1.5,
                                1.5, size=1)
        plot_line(self.ax, X, Y, self.start_x, self.start_y, 1.5, 1.5)

        for x in range(self.border_arr.shape[0]):
            for y in range(self.border_arr.shape[1]):
                color = "g"
                if self.border_arr[x, y, 0]==1:
                    color = (0.5,0,0.5)
                curr_str0 = "curr: " + str(int(x)) + "," + str(int(y))
                curr_str1 = "prev: " + str(int(self.border_arr[x, y, 1])) + "," + str(int(self.border_arr[x, y, 2]))
                curr_str2 = "next: " + str(int(self.border_arr[x, y, 3])) + "," + str(int(self.border_arr[x, y, 4]))
                self.ax.text(x - 0.3, y + 0.4, curr_str0, color=color, fontsize=6)
                self.ax.text(x - 0.3, y + 0.2, curr_str1, color=color, fontsize=6)
                self.ax.text(x - 0.3, y + 0.0, curr_str2, color=color, fontsize=6)
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
            params_arr = [[self.x1, self.y1, 1, curr_en, self.angle, self.test_type]]

            if self.y_cl_plus==0.0:
                R = 1000
            else:
                R = self.y_cl/self.y_cl_plus

            arr_x, arr_y, rarr_x, rarr_y = process_particles(self.counter_arr, self.is_full,
                                             self.border_arr, params_arr, self.Si_num,
                                             self.xsize, self.ysize, R, test=True)
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
            if self.test_x<self.xsize:
                self.test_x+=1
        elif event.key == "left":
            #print("2")
            if self.test_x>0:
                self.test_x-=1
        elif event.key == "down":
            #print("3")
            if self.test_y<self.ysize:
                self.test_y+=1
        elif event.key == "up":
            #print("4")
            if self.test_y>0:
                self.test_y-=1
        elif event.key == "d":
            self.counter_arr[:, self.test_x, self.test_y] = np.array([0,0,0,0])
            self.is_full[self.test_x, self.test_y] = 0
            delete_point(self.border_arr,self.test_x, self.test_y)
        else:
            return None


        self.recheck_cell()
        self.replot()

        #print('Modifier keys:', event.modifier)


    def recheck_cell(self):
        self.master.contPanel.si_lbl["text"] = "Si: " + str(self.counter_arr[0][self.test_x, self.test_y])
        self.master.contPanel.sicl_lbl["text"] = "SiCl: " + str(
            self.counter_arr[1][self.test_x, self.test_y])
        self.master.contPanel.sicl2_lbl["text"] = "SiCl2: " + str(
            self.counter_arr[2][self.test_x, self.test_y])
        self.master.contPanel.sicl3_lbl["text"] = "SiCl3: " + str(
            self.counter_arr[3][self.test_x, self.test_y])
