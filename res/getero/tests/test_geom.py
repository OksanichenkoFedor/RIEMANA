import res.utils.config as config
config.do_njit = False
from res.getero.tests.test_geom_files.tappframe import TestAppFrame
from tkinter import Tk


root = Tk()
app = TestAppFrame()
root.mainloop()