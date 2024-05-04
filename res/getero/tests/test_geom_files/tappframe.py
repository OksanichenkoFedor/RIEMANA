from tkinter.ttk import Frame, Style
from tkinter import BOTH
from res.getero.tests.test_geom_files.tplotframe import TestPlotFrame
from res.getero.tests.test_geom_files.tcpanel import TestControlPanel



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
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        self.plotF = TestPlotFrame(self)
        self.plotF.grid(row=0, column=0, rowspan=4)
        self.contPanel = TestControlPanel(self)
        self.contPanel.grid(row=0, column=1, rowspan=4)
        pass