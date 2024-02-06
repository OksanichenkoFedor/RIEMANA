from tkinter import BOTH
from tkinter.ttk import Frame
from res.frontend.step.plot import StepPlotFrame
from res.parser.parser import Parser
import tkinter as tk
import time

import res.config.step as config


class AppFrame(Frame):

    def __init__(self, filename):
        super().__init__()
        self.parser = Parser(filename)
        self.parser.parsing()
        self.initUI()

    def initUI(self):
        #Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')
        self.pack(fill=BOTH, expand=True)
        #Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.plotF = StepPlotFrame(self)
        self.plotF.grid(row=0, column=0, rowspan=4)
        self.contPanel = ControlPanel(self)
        self.contPanel.grid(row=0, column=1, rowspan=4)


class ControlPanel(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.min_index_entity = tk.IntVar()
        self.max_index_entity = tk.IntVar()
        self.is_all_draw = tk.IntVar()
        self.is_all_draw.set(0)
        self.is_all_draw_lbl = tk.Label(self, text="Draw all")
        self.is_all_draw_lbl.grid(row=0,column=0)
        self.is_all_chk_button = tk.Checkbutton(self, text="Включить", variable=self.is_all_draw)
        self.is_all_chk_button.grid(row=0,column=1)
        self.index_enity_lbl = tk.Label(self, text="Number of entity:")
        self.index_enity_lbl.grid(row=1, column=0)
        self.index_enity_scale = tk.Scale(self, orient='horizontal', from_=0, to=config.max_num_entity)
        self.index_enity_scale.set(config.index_entity)
        self.index_enity_scale.configure(command=self.change_index_entity_scale)
        self.index_enity_scale.grid(row=1, column=1)
        self.b_decrease = tk.Button(self, text="-", width=14, state=tk.NORMAL,
                                    command=self.dec_button)
        self.b_decrease.grid(row=2, column=0)
        self.b_increase = tk.Button(self, text="+", width=14, state=tk.NORMAL,
                                    command=self.inc_button)
        self.b_increase.grid(row=2, column=1)

        self.is_all_draw.trace_add('write', self.change_is_all_d_chkb)
    def change_is_all_d_chkb(self, var, mode, index):
        new_way = self.is_all_draw.get()
        if new_way == 1:
            self.sleep()
            config.plot_all_drawable = True
        else:
            self.wakeUp()
            config.plot_all_drawable = False
        self.master.plotF.replot()

    def change_index_entity_scale(self, scale):

        #print("change_index_entity_scale")
        new_ind = int(self.index_enity_scale.get())
        if config.is_plotting:
            return 0
        config.is_plotting = True
        config.index_entity = new_ind

        self.sleep()
        time2 = time.time()
        self.master.plotF.replot()
        time3 = time.time()
        self.wakeUp()
        config.is_plotting = False

    def inc_button(self):
        old_ind = config.index_entity
        if old_ind == config.max_num_entity:
            pass
        else:
            self.index_enity_scale.set(old_ind + 1)

    def dec_button(self):
        old_ind = config.index_entity
        if old_ind == 0:
            pass
        else:
            self.index_enity_scale.set(old_ind - 1)

    def sleep(self):
        self.b_increase.config(state=tk.DISABLED)
        self.b_decrease.config(state=tk.DISABLED)
        self.index_enity_scale.config(state=tk.DISABLED)

    def wakeUp(self):
        self.b_increase.config(state=tk.NORMAL)
        self.b_decrease.config(state=tk.NORMAL)
        self.index_enity_scale.config(state=tk.NORMAL)
