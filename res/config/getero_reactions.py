multiplier = 0.5

wafer_Si_num = 30
wafer_cell_size = 2.5  # nanometers

wafer_border = int(500 * multiplier)
wafer_xsize = int(2000 * multiplier)
wafer_ysize = int(1800 * multiplier)
wafer_left_area = int(900 * multiplier)
wafer_right_area = int(1100 * multiplier)
wafer_mask_height = int(40 * multiplier)
wafer_y0 = 0
wafer_silicon_size = int(800 * multiplier)

wafer_is_full = None
wafer_counter_arr = None
old_wif = None
old_wca = None

wafer_plot_num = 0
wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]
# wafer_plot_type = "Si"


num_iter = 2500
num_per_iter = 200

T_i = 0.12
T_e = 40 # энергия иона

y_ar_plus = 0.1
y_cl_plus = 0.0
y_cl = 0.9
