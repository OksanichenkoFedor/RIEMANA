multiplier = 1

wafer_Ns = [1,10]
wafer_border = int(500*multiplier)
wafer_xsize = int(2000*multiplier)
wafer_ysize = int(1800*multiplier)
wafer_left_area = int(900*multiplier)
wafer_right_area = int(1100*multiplier)
wafer_mask_height = int(10*multiplier)
wafer_y0 = 0
wafer_silicon_size = int(800*multiplier)

wafer_is_full = None
wafer_counter_arr= None
old_wif = None
old_wca = None

num_iter = 10
num_per_iter = 20000