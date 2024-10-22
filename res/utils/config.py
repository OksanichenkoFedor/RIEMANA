import numpy as np
import numba as nb
from numba.experimental import jitclass

do_njit = False
cache = False
parallel = False

seed = 40
use_seed= False

multiplier = 0.1 # 0.2 примерно топология 180 нм

Si_num = 30
cell_size = 2.5  # nanometers

wafer_plot_num = 0
wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]

num_iter = 2001
num_per_iter = 80000

num_one_side_points = 0


plasma_params = {
    "T_i": 0.12,
    "U_i": 40,
    "j_ar_plus": 1*2.041839429440525e+19,
    "j_cl_plus": 1*1.4431736576424567e+20,
    "j_cl": 1*2.6629180745936804e+22,
    "cell_size": cell_size*(10.0**(-9)),
    "time": 50,
    "a_0": (((1839*28*9.1*10**(-31))/2330)**(1.0/3.0)) #размер одного слоя Si
}

pure_wafer_params = {
    "mask_height": 40,
    "hole_size": 150,
    "border": 500,
    "xsize": 1000,
    "ysize": 2400,
    "silicon_size": 1600
}


min_throw_away_angle = np.pi*(10.0/180.0)

