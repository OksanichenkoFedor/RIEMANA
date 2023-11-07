import matplotlib
import tkinter as tk
import numpy as np
import res.config as config
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from res.const.plot_config import PLOT_ORDER


class PlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=plt.figaspect(0.5))  # , dpi=100, tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.plot()

    def plot(self):
        self.replot()

    def replot(self):
        self.ax = self.f.add_subplot(1, 1, 1, projection='3d')
        # X = np.arange(0, 10, 1)
        # Y = np.arange(0, 10, 1)
        # K, B = np.meshgrid(X, Y)
        # Fs = np.random.random((10, 10))
        # self.a.plot_surface(K, B, Fs)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

        for curr_type in PLOT_ORDER:
            for id in self.master.parser.path_to_entities[curr_type]:
                curr_min, curr_max = self.master.parser.data[id].draw(self.ax)
                new_min = np.concatenate((config.min_coord, curr_min), axis=1)
                config.min_coord = np.min(new_min, axis=1).reshape((3, 1))
                new_max = np.concatenate((config.max_coord, curr_max), axis=1)
                config.max_coord = np.max(new_max, axis=1).reshape((3, 1))

        self.ax.set_xlim(config.min_coord[0, 0], config.max_coord[0, 0])
        self.ax.set_ylim(config.min_coord[1, 0], config.max_coord[1, 0])
        self.ax.set_zlim(config.min_coord[2, 0], config.max_coord[2, 0])

        self.canvas.draw()

    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass
