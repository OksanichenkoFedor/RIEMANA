import numpy as np
import matplotlib.pyplot as plt

from res.getero.algorithm.silicon_reactions.cell_retraction import retract_cell

def test_one(axis):
    count_arr = np.zeros((4,3,3))
    is_f_arr = np.zeros((3,3))
    is_f_arr[1,1] = 1
    is_third = bool(np.random.randint())


    #retract_cell(curr_x, curr_y, counter_arr, is_full_arr, angle, isotropic_retraction)