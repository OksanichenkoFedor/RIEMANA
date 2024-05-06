import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
import time
import numpy as np
from res.utils.config import seed
np.random.seed(seed)

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from res.bot.simple import print_message, throw_plot

import res.utils.config as config
from res.getero.frontend.grafic_funcs import plot_cells, plot_line, plot_animation
from res.getero.algorithm.dynamic_profile import give_line_arrays


class WaferPlotFrame(tk.Frame):
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

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.ax = self.f.add_subplot(1, 1, 1)
        self.plot()

    def plot(self):
        self.replot()

    def replot(self, num=0, do_plot_line = True):
        start = time.time()
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(self.ax, self.master.getero.counter_arr, self.master.getero.is_full,
                   self.master.getero.ysize, self.master.getero.xsize, curr_type)
        X,Y = self.master.getero.profiles[-1]
        if do_plot_line:
            plot_line(self.ax, X, Y, self.master.getero.start_x, self.master.getero.start_y, 0, 0)
        x_major_ticks = np.arange(0, self.master.getero.xsize, 10)+0.5
        x_minor_ticks = np.arange(0, self.master.getero.xsize, 1)+0.5
        y_major_ticks = np.arange(0, self.master.getero.ysize, 10)+0.5
        y_minor_ticks = np.arange(0, self.master.getero.ysize, 1)+0.5
        self.ax.set_xticks(x_major_ticks)
        self.ax.set_xticks(x_minor_ticks, minor=True)
        self.ax.set_yticks(y_major_ticks)
        self.ax.set_yticks(y_minor_ticks, minor=True)
        self.ax.grid(which='minor', alpha=0.2)
        self.ax.grid(which='major', alpha=0.8)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.canvas.draw()
        plot_animation(self.master.getero.profiles, self.master.getero.xsize, self.master.getero.ysize,num)
        end = time.time()
        #print("Plot time: ", round(end-start, 3))



    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass

    def send_picture(self):
        self.f.savefig("tmp.png")
        throw_plot("tmp.png", 710672679)
        throw_plot("tmp.gif", 710672679)
        try:
            pass
        except:
            pass