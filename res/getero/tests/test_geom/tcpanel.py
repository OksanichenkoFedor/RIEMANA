import numpy as np
import tkinter as tk
from tkinter import Tk
from tkinter.ttk import Frame, Style
from tkinter import Entry, Label, BOTH

from res.getero.algorithm.types_of_particle import types

#import res.config.getero_reactions as config


class TestControlPanel(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.type = tk.StringVar()
        self.type_status_text = tk.StringVar()
        self.type_lbl = Label(self, text="Test type: ")
        self.type_lbl.grid(row=0, column=0)
        self.type_ent = Entry(self, textvariable=self.type)
        self.type.set("")
        self.type_ent.grid(row=0, column=1)
        self.type_status_lbl = tk.Label(self, textvariable=self.type_status_text, fg="green")
        self.type_status_text.set("Correct value")
        self.type_status_lbl.grid(row=1, column=0, columnspan=2)

        self.type.trace("w",lambda name, index, mode, status=self.type_status_text, colr=self.type_status_lbl,
                                   value=self.type: self.type_callback(name, index, mode, status, colr,
                                                                               value))

        self.si_lbl = Label(self, text="Si: ")
        self.sicl_lbl = Label(self, text="SiCl: ")
        self.sicl2_lbl = Label(self, text="SiCl2: ")
        self.sicl3_lbl = Label(self, text="SiCl3: ")
        self.si_lbl.grid(row=2, column=0)
        self.sicl_lbl.grid(row=2, column=1)
        self.sicl2_lbl.grid(row=3, column=0)
        self.sicl3_lbl.grid(row=3, column=1)

    def type_callback(self, name, index, mode, status, colr, value):
        good_value = False
        res = value.get()
        if res in types.values():
            good_value = True
        if good_value:
            status.set("Correct value")
            colr.configure(fg="green")
            types_inv = {v: k for k, v in types.items()}
            self.master.plotF.test_type = types_inv[res]
            self.master.plotF.canvas.get_tk_widget().focus_force()
        else:
            status.set("Enter the correct type")
            colr.configure(fg="red")
