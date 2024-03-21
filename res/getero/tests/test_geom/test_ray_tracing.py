import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Tk

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.ttk import Frame, Style
from tkinter import BOTH

import res.config.getero_reactions as config
from res.getero.frontend.grafic_funcs import plot_cells
from res.getero.algorithm.space_orientation import find_prev
from res.getero.tests.test_geom.test_main_cycle import test_process_particles


class TestAppFrame(Frame):

    def __init__(self):
        super().__init__()
        self.style = Style(self)
        self.style.layout("LabeledProgressbar",
                          [('LabeledProgressbar.trough',
                            {'children': [('LabeledProgressbar.pbar',
                                           {'sticky': 'ns'}),
                                          ("LabeledProgressbar.label",  # label inside the bar
                                           {"sticky": ""})],
                             })])
        #self.getero = WaferGenerator(self)
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self.plotF = TestPlotFrame(self)
        self.plotF.grid(row=0, column=0, rowspan=4)
        #self.contPanel = ControlPanel(self)
        #self.contPanel.grid(row=0, column=1, rowspan=4)
        pass


class TestPlotFrame(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        config.multiplier = 0.005
        config.wafer_Si_num = 1
        self.f = Figure(figsize=(9, 9), dpi=100, tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)
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
        is_full = np.fromfunction(lambda i, j: j >= config.wafer_border, (config.wafer_xsize, config.wafer_ysize),
                                  dtype=int).astype(int)
        counter_arr = is_full.copy() * config.wafer_Si_num
        mask = np.ones((config.wafer_xsize, config.wafer_ysize))
        mask[:, :config.wafer_border] = mask[:, :config.wafer_border] * 0
        mask[:,
        config.wafer_border + config.wafer_mask_height:config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] = mask[
                                                                                                                                     :,
                                                                                                                                     config.wafer_border + config.wafer_mask_height:config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] * 0
        mask[config.wafer_left_area:config.wafer_right_area,
        :config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] = mask[
                                                                                       config.wafer_left_area:config.wafer_right_area,
                                                                                       :config.wafer_border + config.wafer_mask_height + config.wafer_silicon_size] * 0
        config.wafer_is_full = mask + is_full
        config.wafer_counter_arr = np.repeat(counter_arr.reshape(1, counter_arr.shape[0], counter_arr.shape[1]), 4,
                                             axis=0)
        config.wafer_counter_arr[1] = config.wafer_counter_arr[1] * 0
        config.wafer_counter_arr[2] = config.wafer_counter_arr[2] * 0
        config.wafer_counter_arr[3] = config.wafer_counter_arr[3] * 0

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
                   config.wafer_ysize, config.wafer_xsize, curr_type)
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
            #print("ddfdfdfdf")
            self.x2 = event.xdata+0.5
            self.y2 = event.ydata+0.5
            self.found = 2
            self.count_angle()
            self.replot()
        elif self.found==2:
            self.replot()
            config.wafer_counter_arr, config.wafer_is_full, arr_x, arr_y = test_process_particles(config.wafer_counter_arr,
                                                                                    config.wafer_is_full,[[self.x1,0,self.angle,False]],
                                                                                    1,config.wafer_xsize,
                                                                                    config.wafer_ysize,self.y1,self.ax)
            self.replot()
            self.ax.plot(arr_x, arr_y,".",color="g")
            self.canvas.draw()
            self.found = 0

    def unclick_mouse_event(self, event):
        self.clicked = False


root = Tk()
app = TestAppFrame()
root.mainloop()