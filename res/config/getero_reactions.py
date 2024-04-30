import numpy as np

multiplier = 0.1

wafer_Si_num = 84
wafer_cell_size = 2.5  # nanometers

wafer_border = int(500 * multiplier)
wafer_xsize = int(2000 * multiplier)
wafer_ysize = int(2400 * multiplier)
wafer_left_area = int(800 * multiplier)
wafer_right_area = int(1200 * multiplier)
wafer_mask_height = int(100 * multiplier)
wafer_y0 = 0
wafer_silicon_size = int(1600 * multiplier)

test_x = 0
test_y = 0
test_type = 0

wafer_is_full = None
wafer_counter_arr = None
wafer_border_arr = None
old_wif = None
old_wca = None
start_x, start_y = None, None
end_x, end_y = None, None

wafer_plot_num = 0
wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]
# wafer_plot_type = "Si"


num_iter = 2500
num_per_iter = 2000

T_i = 0.12
T_e = 40 # энергия иона

y_ar_plus = 0.1
y_cl_plus = 0.1
y_cl = 0.8

otn_const = 1.0/np.log(8)
