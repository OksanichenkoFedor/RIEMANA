from res.global_entities.wafer import Wafer
from res.global_entities.plotter import generate_figure
#from res.getero.tests.test_productivity import count_time

import matplotlib.pyplot as plt


wafer = Wafer()
#wafer.load("../files/test_wafer_16000.zip")
#wafer.load("../files/test_wafer_half.zip")
wafer.load("../files/test_wafer_after_half.zip")

#wafer.generate_pure_wafer(0.01, 84)
#print("xsize: ",wafer.xsize)

#f = generate_figure(wafer, wafer_curr_type="is_cell", do_plot_line=True)

wafer.make_half()

f = generate_figure(wafer, wafer_curr_type="is_cell", do_plot_line=True)
#wafer.save("../files/test_wafer_half_small.zip")

wafer = Wafer()
wafer.load("../files/test_wafer_half.zip")


#wafer.return_half()

f = generate_figure(wafer, wafer_curr_type="is_cell", do_plot_line=True)

#wafer.save("../files/test_wafer_after_half.zip")

plt.show()

