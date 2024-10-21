from tkinter import BOTH
from tkinter.ttk import Frame, Style

from res.global_entities.plotter import Plotter
from res.global_entities.control_panel import ControlPanel
from res.global_entities.etcher import Etcher

class MainFrame(Frame):

    def __init__(self, multiplier, consts_filename="data/plasma_cl2_ar_data.csv"):
        super().__init__()
        self.num_iter = 3010
        self.wafer_curr_type = "is_cell"
        self.wafer_plot_num = 0
        self.wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]
        self.params = {
            "p_0": 10 * 0.13333,
            "T_gas": 600,
            "R": 0.15,
            "L": 0.14,
            "gamma_cl": 0.02,
            "y_ar": 0.1,
            "W": 600,
            "U_i": 200,
            "time": 0.5,
            "do_half": False,
        }
        self.const_params = {
            "a_0": ((1839*28*9.1*10**(-31))/2330)**(1.0/3.0),
            "cell_size":  2.5*(10.0**(-9)),

        }
        self.contPanel = ControlPanel(self)
        self.plotter = Plotter(self)
        self.etcher = Etcher(multiplier, consts_filename=consts_filename)
        self.initUI()
        if False:
            print("Startnew! y_ar", self.params["y_ar"])
            self.etcher.init()
            self.params["U_i"] = 200
            self.params["y_ar"] = 0.1
            self.etcher.run(self.params)
            self.plotter.replot(self.etcher.wafer)

            print("Startnew! y_ar", self.params["y_ar"])
            self.etcher.init()
            self.params["U_i"] = 200
            self.params["y_ar"] = 0.5
            self.etcher.run(self.params)
            self.plotter.replot(self.etcher.wafer)

            print("Startnew! y_ar", self.params["y_ar"])
            self.etcher.init()
            self.params["U_i"] = 200
            self.params["y_ar"] = 0.9
            self.etcher.run(self.params)
            self.plotter.replot(self.etcher.wafer)




    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self.plotter.grid(row=0, column=0, rowspan=4)
        self.contPanel = ControlPanel(self)
        self.contPanel.grid(row=0, column=1, rowspan=4)
        self.plotter.replot(self.etcher.wafer)

    def change_wafer_plot_type(self):
        self.wafer_plot_num = (self.wafer_plot_num + 1) % len(self.wafer_plot_types)
        self.wafer_curr_type = self.wafer_plot_types[self.wafer_plot_num]