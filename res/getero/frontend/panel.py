from tkinter import BOTH
from tkinter.ttk import Frame, Style
import tkinter as tk
from tkinter import Entry, Label
from tkinter.ttk import Progressbar

import res.config.getero_reactions as config
from res.getero.algorithm.wafer_generator import WaferGenerator
from res.getero.frontend.wafer_plot import WaferPlotFrame


class AppFrame(Frame):

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
        self.getero = WaferGenerator(self)
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self.plotF = WaferPlotFrame(self)
        self.plotF.grid(row=0, column=0, rowspan=4)
        self.contPanel = ControlPanel(self)
        self.contPanel.grid(row=0, column=1, rowspan=4)


class ControlPanel(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.num_iter = tk.StringVar()
        self.num_iter_status_text = tk.StringVar()
        self.num_iter_lbl = Label(self, text="Number of iterations: ")
        self.num_iter_lbl.grid(row=0, column=0)
        self.num_iter_ent = Entry(self, textvariable=self.num_iter)
        self.num_iter.set(config.num_iter)
        self.num_iter_ent.grid(row=0, column=1)
        self.num_iter_status_lbl = tk.Label(self, textvariable=self.num_iter_status_text, fg="green")
        self.num_iter_status_text.set("Correct value")
        self.num_iter_status_lbl.grid(row=1, column=0, columnspan=2)
        self.num_iter.trace("w",
                            lambda name, index, mode, status=self.num_iter_status_text, colr=self.num_iter_status_lbl,
                                   value=self.num_iter: self.num_iter_callback(name, index, mode, status, colr,
                                                                               value))

        self.num_per_iter = tk.StringVar()
        self.num_per_iter_status_text = tk.StringVar()
        self.num_per_iter_lbl = Label(self, text="Number of particles per iteration: ")
        self.num_per_iter_lbl.grid(row=2, column=0)
        self.num_per_iter_ent = Entry(self, textvariable=self.num_per_iter)
        self.num_per_iter.set(config.num_per_iter)
        self.num_per_iter_ent.grid(row=2, column=1)
        self.num_per_iter_status_lbl = tk.Label(self, textvariable=self.num_per_iter_status_text, fg="green")
        self.num_per_iter_status_text.set("Correct value")
        self.num_per_iter_status_lbl.grid(row=3, column=0, columnspan=2)
        self.num_per_iter.trace("w",
                                lambda name, index, mode, status=self.num_per_iter_status_text,
                                       colr=self.num_per_iter_status_lbl,
                                       value=self.num_per_iter: self.num_per_iter_callback(name, index, mode, status,
                                                                                           colr,
                                                                                           value))

        self.progress_var = tk.IntVar()
        self.bsim = tk.Button(self, text="Simulate", width=14, state=tk.NORMAL,
                              command=self.simulate)
        self.bsim.grid(row=4, column=0)

        self.bback = tk.Button(self, text="Back", width=14, state=tk.DISABLED,
                               command=self.go_back)
        self.bback.grid(row=4, column=1)

        self.progress_bar = Progressbar(self, orient="horizontal", maximum=10, mode="determinate",
                                        var=self.progress_var, style="LabeledProgressbar")
        self.master.style.configure("LabeledProgressbar", text="0/0")
        self.progress_var.set(0)
        self.progress_bar.update()
        self.progress_bar.grid(row=5, column=0, columnspan=2)

        self.bchange_type = tk.Button(self, text="Change type", width=14, state=tk.NORMAL,
                                      command=self.change_type)
        self.bchange_type.grid(row=6, column=0, columnspan=2)

    def simulate(self):
        self.sleep()
        self.master.getero.run(config.num_iter, config.num_per_iter)
        self.master.plotF.replot()
        self.master.plotF.send_picture()
        self.wakeUp()
        self.bback.config(state=tk.NORMAL)

    def go_back(self):
        self.sleep()
        print("Back!!!")
        print(config.wafer_is_full is config.old_wif)
        config.wafer_is_full = config.old_wif.copy()
        config.wafer_counter_arr = config.old_wca.copy()
        self.master.plotF.replot()
        self.wakeUp()
        self.bback.config(state=tk.DISABLED)

    def num_iter_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            num_iter = int(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if num_iter >= 1:
                config.num_iter = num_iter
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("Number of iterations must be equal or more than 1")
                colr.configure(fg="red")
        else:
            status.set("Enter the integer number")
            colr.configure(fg="red")

    def num_per_iter_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            num_per_iter = int(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if num_per_iter >= 1:
                config.num_per_iter = num_per_iter
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("Number of particles per iteration must be equal or more than 1")
                colr.configure(fg="red")
        else:
            status.set("Enter the integer number")
            colr.configure(fg="red")

    def sleep(self):
        self.bsim.config(state=tk.DISABLED)
        self.bback.config(state=tk.DISABLED)
        self.bchange_type.config(state=tk.DISABLED)
        self.num_iter_ent.config(state=tk.DISABLED)
        self.num_per_iter_ent.config(state=tk.DISABLED)

    def wakeUp(self):
        self.bsim.config(state=tk.NORMAL)
        self.bback.config(state=tk.NORMAL)
        self.bchange_type.config(state=tk.NORMAL)
        self.num_iter_ent.config(state=tk.NORMAL)
        self.num_per_iter_ent.config(state=tk.NORMAL)

    def change_type(self):
        config.wafer_plot_num = (config.wafer_plot_num + 1) % len(config.wafer_plot_types)
        self.sleep()
        self.master.plotF.replot()
        self.wakeUp()
