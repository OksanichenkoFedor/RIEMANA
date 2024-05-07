from tkinter import BOTH
from tkinter.ttk import Frame, Style
import tkinter as tk
from tkinter import Entry, Label
from tkinter.ttk import Progressbar


class ControlPanel(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.style = Style(self)
        self.style.layout("LabeledProgressbar",
                          [('LabeledProgressbar.trough',
                            {'children': [('LabeledProgressbar.pbar',
                                           {'sticky': 'ns'}),
                                          ("LabeledProgressbar.label",  # label inside the bar
                                           {"sticky": ""})],
                             })])
        self.initUI()

    def initUI(self):

        self.num_iter = tk.StringVar()
        self.num_iter_status_text = tk.StringVar()
        self.num_iter_lbl = Label(self, text="Number of iterations: ")
        self.num_iter_lbl.grid(row=0, column=0)
        self.num_iter_ent = Entry(self, textvariable=self.num_iter)
        self.num_iter.set(self.master.num_iter)
        self.num_iter_ent.grid(row=0, column=1)
        self.num_iter_status_lbl = tk.Label(self, textvariable=self.num_iter_status_text, fg="green")
        self.num_iter_status_text.set("Correct value")
        self.num_iter_status_lbl.grid(row=1, column=0, columnspan=2)
        self.num_iter.trace("w",
                            lambda name, index, mode, status=self.num_iter_status_text, colr=self.num_iter_status_lbl,
                                   value=self.num_iter: self.num_iter_callback(name, index, mode, status, colr,
                                                                               value))

        self.time_v = tk.StringVar()
        self.time_status_text = tk.StringVar()
        self.time_lbl = Label(self, text="Time(s): ")
        self.time_lbl.grid(row=2, column=0)
        self.time_ent = Entry(self, textvariable=self.time_v)
        self.time_v.set(self.master.time)
        self.time_ent.grid(row=2, column=1)
        self.time_status_lbl = tk.Label(self, textvariable=self.time_status_text, fg="green")
        self.time_status_text.set("Correct value")
        self.time_status_lbl.grid(row=3, column=0, columnspan=2)
        self.time_v.trace("w",
                                lambda name, index, mode, status=self.time_status_text,
                                       colr=self.time_status_lbl,
                                       value=self.time_v: self.time_callback(name, index, mode, status,
                                                                                           colr,
                                                                                           value))

        self.progress_var = tk.IntVar()
        self.bsim = tk.Button(self, text="Simulate", width=14, state=tk.NORMAL,
                              command=self.simulate)
        self.bsim.grid(row=4, column=0, columnspan=2)

        #self.bback = tk.Button(self, text="Back", width=14, state=tk.DISABLED,
        #                       command=self.go_back)
        #self.bback.grid(row=4, column=1)

        self.progress_bar = Progressbar(self, orient="horizontal", maximum=10, mode="determinate",
                                        var=self.progress_var, style="LabeledProgressbar")
        self.style.configure("LabeledProgressbar", text="0/0")
        self.progress_var.set(0)
        self.progress_bar.update()
        self.progress_bar.grid(row=5, column=0, columnspan=2)

        self.bchange_type = tk.Button(self, text="Change type", width=14, state=tk.NORMAL,
                                      command=self.change_type)
        self.bchange_type.grid(row=6, column=0, columnspan=2)

    def simulate(self):
        self.sleep()
        self.master.run()
        #self.master.plotF.replot()
        #self.master.plotF.send_picture()
        self.wakeUp()

    def num_iter_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            num_iter = int(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if num_iter >= 1:
                self.master.num_iter = num_iter
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("Number of iterations must be equal or more than 1")
                colr.configure(fg="red")
        else:
            status.set("Enter the integer number")
            colr.configure(fg="red")

    def time_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            time = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if time > 0:
                self.master.time = time
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("Number of particles per iteration must be more than 0")
                colr.configure(fg="red")
        else:
            status.set("Enter the number")
            colr.configure(fg="red")

    def sleep(self):
        self.bsim.config(state=tk.DISABLED)
        self.bchange_type.config(state=tk.DISABLED)
        self.num_iter_ent.config(state=tk.DISABLED)
        self.time_ent.config(state=tk.DISABLED)

    def wakeUp(self):
        self.bsim.config(state=tk.NORMAL)
        self.bchange_type.config(state=tk.NORMAL)
        self.num_iter_ent.config(state=tk.NORMAL)
        self.time_ent.config(state=tk.NORMAL)

    def change_type(self):

        self.master.change_wafer_plot_type()
        self.sleep()
        self.master.plotF.replot()
        self.wakeUp()