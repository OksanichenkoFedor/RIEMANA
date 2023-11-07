from tkinter import BOTH
from tkinter.ttk import Frame, Style
from res.frontend.plot import PlotFrame
from res.parser.parser import Parser

class AppFrame(Frame):

    def __init__(self, filename):
        super().__init__()
        self.parser = Parser(filename)
        self.parser.parsing()
        self.initUI()




    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.plotF = PlotFrame(self)
        self.plotF.grid(row=0, column=0, rowspan=4)