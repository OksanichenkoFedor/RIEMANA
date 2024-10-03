import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk


from res.getero.frontend.grafic_funcs import plot_cells, plot_line, plot_animation
from res.bot.simple import print_message, throw_plot
from res.getero.algorithm.dynamic_profile import give_line_arrays

class Plotter(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        #self.initUI()

    def replot(self, wafer, do_plot_line=True):

        self.f = generate_figure(wafer, self.master.wafer_curr_type, do_plot_line)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)
        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.canvas.draw()

    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass


def generate_figure(wafer, wafer_curr_type, do_plot_line=True):
    f = plt.figure(figsize=(13, 13), dpi=100, tight_layout=True)
    axis = f.add_subplot(1, 1, 1)
    start = time.time()
    axis.clear()
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    # curr_type = config.wafer_plot_types[config.wafer_plot_num]
    plot_cells(axis, wafer.counter_arr, wafer.is_full, wafer.ysize, wafer.xsize, wafer_curr_type)
    X, Y = give_line_arrays(wafer.border_arr, wafer.is_half)
    if do_plot_line:
        plot_line(axis, X, Y, 0, 0, do_points=False)
    for x in range(wafer.border_arr.shape[0]):
        for y in range(wafer.border_arr.shape[1]):
            color = "g"
            if wafer.border_arr[x, y, 0] == 1:
                color = (0.5, 0, 0.5)
            curr_str0 = "curr: " + str(int(x)) + "," + str(int(y))
            curr_str1 = "prev: " + str(int(wafer.border_arr[x, y, 1])) + "," + str(int(wafer.border_arr[x, y, 2]))
            curr_str2 = "next: " + str(int(wafer.border_arr[x, y, 3])) + "," + str(int(wafer.border_arr[x, y, 4]))
            #axis.text(x - 0.3, y + 0.4, curr_str0, color=color, fontsize=5)
            #axis.text(x - 0.3, y + 0.2, curr_str1, color=color, fontsize=5)
            #axis.text(x - 0.3, y + 0.0, curr_str2, color=color, fontsize=5)
            #axis.text(x - 0.3, y + 0.2, str(int(wafer.border_arr[x, y, 0])), color=color, fontsize=9)

    x_major_ticks = np.arange(0, wafer.xsize, 10) + 0.5
    x_minor_ticks = np.arange(0, wafer.xsize, 1) + 0.5
    y_major_ticks = np.arange(0, wafer.ysize, 10) + 0.5
    y_minor_ticks = np.arange(0, wafer.ysize, 1) + 0.5
    axis.set_xticks(x_major_ticks)
    axis.set_xticks(x_minor_ticks, minor=True)
    axis.set_yticks(y_major_ticks)
    axis.set_yticks(y_minor_ticks, minor=True)
    axis.grid(which='minor', alpha=0.2)
    axis.grid(which='major', alpha=0.8)
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    end = time.time()
    print("Plot time: ", round(end - start, 3))

    return f