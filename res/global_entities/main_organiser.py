from tkinter import BOTH
from tkinter.ttk import Frame, Style

from res.global_entities.etcher import Etcher
from res.global_entities.plotter import Plotter
from res.global_entities.control_panel import ControlPanel
from res.global_entities.plasmer import Plasmer
from res.global_entities.wafer import Wafer

class MainFrame(Frame):

    def __init__(self, multiplier, consts_filename="data/data.csv"):
        super().__init__()
        self.num_iter = 3010
        self.wafer_curr_type = "is_cell"
        self.wafer_plot_num = 0
        self.wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]
        self.time = 60
        self.params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.5,
            "W": 600,
            "U_i": 500
        }
        self.const_params = {
            "a_0": ((1839*28*9.1*10**(-31))/2330)**(1.0/3.0),
            "cell_size":  2.5*(10.0**(-9)),

        }
        self.etcher = Etcher()
        self.contPanel = ControlPanel(self)
        self.plotter = Plotter(self)
        self.wafer = Wafer(multiplier)
        self.plasmer = Plasmer(consts_filename)
        #self.initUI()
        self.params["U_i"] = 100
        print("Startnew! ",self.params["U_i"])
        self.run(do_print=False)
        self.wafer = Wafer(multiplier)
        self.params["U_i"] = 200
        print("Startnew! ", self.params["U_i"])
        self.run(do_print=False)
        self.wafer = Wafer(multiplier)
        self.params["U_i"] = 300
        print("Startnew! ", self.params["U_i"])
        self.run(do_print=False)
        self.params["U_i"] = 400
        print("Startnew! ", self.params["U_i"])
        self.run(do_print=False)
        self.wafer = Wafer(multiplier)
        self.params["U_i"] = 100
        self.params["y_ar"] = 0.1
        print("Startnew! y_ar", self.params["y_ar"])
        self.run(do_print=False)
        self.wafer = Wafer(multiplier)
        self.params["U_i"] = 100
        self.params["y_ar"] = 0.9
        print("Startnew! y_ar", self.params["y_ar"])
        self.run(do_print=False)



    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self.plotter.grid(row=0, column=0, rowspan=4)
        self.contPanel = ControlPanel(self)
        self.contPanel.grid(row=0, column=1, rowspan=4)
        #self.plotter.replot(self.wafer)

    def run(self, do_print=True):
        plasma_params = self.plasmer.count_plasma(self.params)
        plasma_params.update(self.const_params)
        plasma_params.update(self.params)
        self.etcher.change_plasma_params(plasma_params)
        if do_print:
            self.etcher.run(self.wafer, self.time, self.num_iter, self.contPanel, self.plotter)
        else:
            self.etcher.run(self.wafer, self.time, self.num_iter, plotter=self.plotter, do_print=False)
        self.plotter.replot(self.wafer, do_plot_line=True)

    def change_wafer_plot_type(self):
        self.wafer_plot_num = (self.wafer_plot_num + 1) % len(self.wafer_plot_types)
        self.wafer_curr_type = self.wafer_plot_types[self.wafer_plot_num]