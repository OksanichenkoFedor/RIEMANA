import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
import time

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from res.bot.simple import print_message, throw_plot

import res.utils.config as config
from res.getero.frontend.grafic_funcs import plot_cells, plot_line
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

    def replot(self):
        start = time.time()
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(self.ax, self.master.getero.counter_arr, self.master.getero.is_full,
                   self.master.getero.ysize, self.master.getero.xsize, curr_type)
        X, Y = give_line_arrays(self.master.getero.border_arr, self.master.getero.start_x, self.master.getero.start_y,
                                self.master.getero.end_x, self.master.getero.end_y, 1, 1, size=1)
        plot_line(self.ax, X, Y, self.master.getero.start_x, self.master.getero.start_y, 1, 1)
        self.canvas.draw()
        end = time.time()
        print("Plot time: ", round(end-start, 3))



    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass

    def send_picture(self):
        print_message("test", 710672679)
        self.f.savefig("tmp.png")
        throw_plot("tmp.png", 710672679)
        try:
            pass
        except:
            pass