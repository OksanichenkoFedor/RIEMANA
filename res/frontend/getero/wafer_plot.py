import matplotlib
import tkinter as tk
import numpy as np


matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


import res.config.getero_reactions as config
from res.getero.grafic_funcs import plot_cells


class WaferPlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=(13, 13), dpi=100, tight_layout=True)
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
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        plot_cells(self.ax, config.wafer_is_full, config.wafer_ysize, config.wafer_xsize)
        self.canvas.draw()


    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass