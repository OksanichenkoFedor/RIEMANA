import matplotlib
import tkinter as tk
import numpy as np
import res.config.step as config

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from res.const.plot_config import PLOT_ORDER
from res.step.parser.entities.ancestors import Drawable


class StepPlotFrame(tk.Frame):
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
        self.ax = self.f.add_subplot(1, 1, 1, projection='3d')
        self.ax.set_box_aspect((1, 1, 1))
        self.plot()

    def plot(self):
        self.replot()

    def replot(self):
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        curr_num = 0
        for curr_type in PLOT_ORDER:
            if curr_type in self.master.parser.path_to_entities:
                for id in self.master.parser.path_to_entities[curr_type]:
                    is_plotting = (curr_num == config.index_entity or config.plot_all_drawable)
                    if not isinstance(self.master.parser.data[id], Drawable):
                        raise ValueError('Expected Drawable, got ', type(self.master.parser.data[id]))
                    curr_min, curr_max = self.master.parser.data[id].draw(self.ax, color=None, is_plotting=is_plotting)
                    new_min = np.concatenate((config.min_coord, curr_min), axis=1)
                    config.min_coord = np.min(new_min, axis=1).reshape((3, 1))
                    new_max = np.concatenate((config.max_coord, curr_max), axis=1)
                    config.max_coord = np.max(new_max, axis=1).reshape((3, 1))
                    curr_num += 1
        mid_coord = 0.5 * (config.max_coord + config.min_coord)
        delta = 0.5 * np.max(config.max_coord - config.min_coord)
        min_coord = mid_coord - delta
        max_coord = mid_coord + delta
        self.ax.set_xlim(min_coord[0, 0], max_coord[0, 0])
        self.ax.set_ylim(min_coord[1, 0], max_coord[1, 0])
        self.ax.set_zlim(min_coord[2, 0], max_coord[2, 0])

        self.canvas.draw()

    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass
